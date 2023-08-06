# Rekall Memory Forensics
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

"""This plugin adds the ability for Rekall to acquire an AFF4 image.

It is an alternative to the pmem suite of acquisition tools, which also creates
AFF4 images. The difference being that this plugin will apply live analysis to
acquire more relevant information (e.g. mapped files etc).
"""

__author__ = "Michael Cohen <scudette@google.com>"

import os
import posixpath
import re
import stat
import time

from rekall import constants
from rekall import plugin
from rekall import testlib
from rekall import utils
from rekall import yaml_utils
from rekall.plugins import core

from pyaff4 import data_store
from pyaff4 import aff4_image
from pyaff4 import aff4_map
from pyaff4 import zip
from pyaff4 import lexicon
from pyaff4 import rdfvalue

from pyaff4 import plugins  # pylint: disable=unused-import


class AFF4Acquire(plugin.Command):
    """Copy the physical address space to an AFF4 file.


    NOTE: This plugin does not required a working profile - unless the user also
    wants to copy the pagefile or mapped files. In that case we must analyze the
    live memory to gather the required files.
    """

    name = "aff4acquire"

    BUFFERSIZE = 1024 * 1024

    PROFILE_REQUIRED = False

    @classmethod
    def args(cls, parser):
        super(AFF4Acquire, cls).args(parser)

        parser.add_argument(
            "destination", default="output.aff4", required=False,
            help="The destination file to create. "
            "If not specified we write output.aff4 in current directory.")

        parser.add_argument(
            "--compression", default="snappy", required=False,
            choices=["snappy", "stored", "zlib"],
            help="The compression to use.")

        parser.add_argument(
            "--also_files", default=False, type="Boolean",
            help="Also get mapped or opened files (requires a profile)")

        parser.add_argument(
            "--also_pagefile", default=False, type="Boolean",
            help="Also get the pagefile/swap partition (requires a profile)")

    def __init__(self, destination=None, compression="snappy", also_files=False,
                 also_pagefile=False, max_file_size=100*1024*1024, **kwargs):
        super(AFF4Acquire, self).__init__(**kwargs)

        self.destination = destination or "output.aff4"
        if compression == "snappy" and aff4_image.snappy:
            compression = lexicon.AFF4_IMAGE_COMPRESSION_SNAPPY
        elif compression == "stored":
            compression = lexicon.AFF4_IMAGE_COMPRESSION_STORED
        elif compression == "zlib":
            compression = lexicon.AFF4_IMAGE_COMPRESSION_ZLIB
        else:
            raise plugin.PluginError(
                "Compression scheme not supported.")

        self.compression = compression
        self.also_files = also_files
        self.also_pagefile = also_pagefile
        self.max_file_size = max_file_size

    def copy_physical_address_space(self, renderer, resolver, volume):
        """Copies the physical address space to the output volume."""
        image_urn = volume.urn.Append("PhysicalMemory")
        source = self.session.physical_address_space

        # Mark the stream as a physical memory stream.
        resolver.Set(image_urn, lexicon.AFF4_CATEGORY,
                     rdfvalue.URN(lexicon.AFF4_MEMORY_PHYSICAL))

        if self.compression:
            storage_urn = image_urn.Append("data")
            resolver.Set(storage_urn, lexicon.AFF4_IMAGE_COMPRESSION,
                         rdfvalue.URN(self.compression))

        with volume.CreateMember(
                image_urn.Append("information.yaml")) as metadata_fd:

            metadata_fd.Write(
                yaml_utils.encode(self.create_metadata(source)))

        renderer.format("Imaging Physical Memory:\n")

        with aff4_map.AFF4Map.NewAFF4Map(
            resolver, image_urn, volume.urn) as image_stream:

            total = 0
            last_tick = time.time()

            for offset, _, length in source.get_address_ranges():
                image_stream.seek(offset)

                while length > 0:
                    to_read = min(length, self.BUFFERSIZE)
                    data = source.read(offset, to_read)

                    image_stream.write(data)
                    now = time.time()

                    read_len = len(data)
                    if now > last_tick:
                        rate = read_len / (now - last_tick) / 1e6
                    else:
                        rate = 0

                    self.session.report_progress(
                        "%s: Wrote %#x (%d mb total) (%02.2d Mb/s)",
                        source, offset, total / 1e6, rate)

                    length -= read_len
                    offset += read_len
                    total += read_len
                    last_tick = now

        resolver.Close(image_stream)
        renderer.format("Wrote {0} mb of Physical Memory to {1}\n",
                        total/1024/1024, image_stream.urn)

    def _copy_address_space(self, renderer, resolver, volume, image_urn,
                            source):
        if self.compression:
            resolver.Set(image_urn, lexicon.AFF4_IMAGE_COMPRESSION,
                         rdfvalue.URN(self.compression))

        with aff4_image.AFF4Image.NewAFF4Image(
            resolver, image_urn, volume.urn) as image_stream:

            total = 0
            last_tick = time.time()

            for offset, _, length in source.get_address_ranges():
                while length > 0:
                    to_read = min(length, self.BUFFERSIZE)
                    data = source.read(offset, to_read)

                    image_stream.write(data)
                    now = time.time()

                    read_len = len(data)
                    if now > last_tick:
                        rate = read_len / (now - last_tick) / 1e6
                    else:
                        rate = 0

                    self.session.report_progress(
                        "%s: Wrote %#x (%d total) (%02.2d Mb/s)",
                        source, offset, total / 1e6, rate)

                    length -= read_len
                    offset += read_len
                    total += read_len
                    last_tick = now

        resolver.Close(image_stream)
        renderer.format("Wrote {0} ({1} mb)\n", source.name, total/1024/1024)

    def linux_copy_files(self, renderer, resolver, volume):
        """Copy all the mapped or opened files to the volume."""
        # Build a set of all files.
        vma_files = set()
        filenames = set()

        for task in self.session.plugins.pslist().filter_processes():
            for vma in task.mm.mmap.walk_list("vm_next"):
                vm_file_offset = vma.vm_file.obj_offset
                if vm_file_offset in vma_files:
                    continue

                filename = task.get_path(vma.vm_file)
                if filename in filenames:
                    continue

                try:
                    stat_entry = os.stat(filename)
                except (OSError, IOError):
                    continue

                mode = stat_entry.st_mode
                if (stat.S_ISREG(mode) and
                        stat_entry.st_size <= self.max_file_size):
                    filenames.add(filename)
                    vma_files.add(vm_file_offset)

                    self._copy_file_to_image(
                        renderer, resolver, volume, filename)

    def _copy_file_to_image(self, renderer, resolver, volume, filename):
        image_urn = volume.urn.Append(utils.SmartStr(filename))
        out_fd = None
        try:
            with open(filename, "rb") as in_fd:
                with aff4_image.AFF4Image.NewAFF4Image(
                    resolver, image_urn, volume.urn) as out_fd:

                    renderer.format("Adding file {0}\n", filename)
                    resolver.Set(
                        image_urn, lexicon.AFF4_STREAM_ORIGINAL_FILENAME,
                        rdfvalue.XSDString(filename))

                    while 1:
                        data = in_fd.read(self.BUFFERSIZE)
                        if not data:
                            break

                        out_fd.write(data)

        except IOError:
            try:
                self.session.logging.debug(
                    "Unable to read %s. Attempting raw access.", filename)

                # We can not just read this file, parse it from the NTFS.
                self._copy_raw_file_to_image(
                    renderer, resolver, volume, filename)
            except IOError:
                self.session.logging.warn(
                    "Unable to read %s. Skipping.", filename)


        finally:
            if out_fd:
                resolver.Close(out_fd)

    def _copy_raw_file_to_image(self, renderer, resolver, volume, filename):
        image_urn = volume.urn.Append(utils.SmartStr(filename))

        drive, base_filename = os.path.splitdrive(filename)
        if not base_filename:
            return

        ntfs_session = self.session.add_session(
            filename=r"\\.\%s" % drive,
            profile="ntfs")

        ntfs_session.plugins.istat(2)

        ntfs = ntfs_session.GetParameter("ntfs")
        mft_entry = ntfs.MFTEntryByName(base_filename)
        data_as = mft_entry.open_file()

        self._copy_address_space(renderer, resolver, volume, image_urn, data_as)

        resolver.Set(image_urn, lexicon.AFF4_STREAM_ORIGINAL_FILENAME,
                     rdfvalue.XSDString(filename))

    def windows_copy_files(self, renderer, resolver, volume):
        filenames = set()

        for task in self.session.plugins.pslist().filter_processes():
            for vad in task.RealVadRoot.traverse():
                try:
                    file_obj = vad.ControlArea.FilePointer
                    file_name = file_obj.file_name_with_drive()
                    if not file_name:
                        continue

                except AttributeError:
                    continue

                if file_name in filenames:
                    continue

                filenames.add(file_name)
                self._copy_file_to_image(renderer, resolver, volume, file_name)

        object_tree_plugin = self.session.plugins.object_tree()
        for module in self.session.plugins.modules().lsmod():
            try:
                path = object_tree_plugin.FileNameWithDrive(
                    module.FullDllName.v())

                self._copy_file_to_image(renderer, resolver, volume, path)
            except IOError:
                self.session.logging.debug(
                    "Unable to read %s. Skipping.", path)


    def copy_files(self, renderer, resolver, volume):
        # Forces profile autodetection if needed.
        profile = self.session.profile

        os_name = profile.metadata("os")
        if os_name == "windows":
            self.windows_copy_files(renderer, resolver, volume)
        elif os_name == "linux":
            self.linux_copy_files(renderer, resolver, volume)


    def copy_page_file(self, renderer, resolver, volume):
        pagefiles = self.session.GetParameter("pagefiles")
        for filename, _ in pagefiles.values():
            renderer.format("Imaging pagefile {0}\n", filename)
            self._copy_raw_file_to_image(
                renderer, resolver, volume, filename)

    def create_metadata(self, source):
        """Returns a dict with a standard metadata format.

        We gather data from the session.
        """
        result = dict(Imager="Rekall %s (%s)" % (constants.VERSION,
                                                 constants.CODENAME),
                      Registers={},
                      Runs=[])

        if self.session.HasParameter("dtb"):
            result["Registers"]["CR3"] = self.session.GetParameter("dtb")

        if self.session.HasParameter("kernel_base"):
            result["KernBase"] = self.session.GetParameter("kernel_base")

        for vaddr, _, length in source.get_address_ranges():
            result["Runs"].append(dict(start=vaddr, length=length))

        return result

    def render(self, renderer):
        if self.compression:
            renderer.format("Will use compression: {0}\n", self.compression)

        # If no address space is specified we try to operate in live mode.
        if self.session.plugins.load_as().GetPhysicalAddressSpace() == None:
            renderer.format("Will load physical address space from live plugin.")
            live = self.session.plugins.live()
            try:
                live.live()
                self.render_acquisition(renderer)
            finally:
                live.close()
        else:
            self.render_acquisition(renderer)

    def render_acquisition(self, renderer):
        with renderer.open(filename=self.destination, mode="w+b") as out_fd:
            with data_store.MemoryDataStore() as resolver:
                output_urn = rdfvalue.URN.FromFileName(out_fd.name)
                resolver.Set(output_urn, lexicon.AFF4_STREAM_WRITE_MODE,
                             rdfvalue.XSDString("truncate"))

                with zip.ZipFile.NewZipFile(resolver, output_urn) as volume:
                    self.copy_physical_address_space(renderer, resolver, volume)

                    # We only copy files if we are running on a raw device.
                    if self.session.physical_address_space.volatile:
                        self.copy_page_file(renderer, resolver, volume)
                        if self.also_files:
                            self.copy_files(renderer, resolver, volume)

# We can not check the file hash because AFF4 files contain UUID which will
# change each time.
class TestAFF4Acquire(testlib.SimpleTestCase):
    PARAMETERS = dict(commandline="aff4acquire %(tempdir)s/output_image.aff4")

    def filter(self, output):
        result = []
        for line in output:
            result.append(re.sub("aff4:/+[^/]+/", "aff4:/XXXX/", line))
        return result

    def testCase(self):
        """AFF4 uses GUIDs which vary all the time."""
        previous = self.filter(self.baseline['output'])
        current = self.filter(self.current['output'])

        # Compare the entire table
        self.assertEqual(previous, current)


class AFF4Ls(plugin.Command):
    """List the content of an AFF4 file."""

    name = "aff4ls"

    @classmethod
    def args(cls, parser):
        super(AFF4Ls, cls).args(parser)

        parser.add_argument(
            "-l", "--long", default=False, type="Boolean",
            help="Include additional information about each stream.")

        parser.add_argument(
            "volume", default=None, required=True,
            help="Volume to list.")

    def __init__(self, long=False, volume=None, **kwargs):
        super(AFF4Ls, self).__init__(**kwargs)
        self.long = long
        self.volume_path = volume
        self.resolver = data_store.MemoryDataStore()

    def render_long(self, renderer, volume):
        """Render a detailed description of the contents of an AFF4 volume."""
        renderer.table_header([
            dict(name="Size", width=15),
            dict(name="Original Name", width=50),
            dict(name="URN", width=150),
        ])

        for subject in self.resolver.QuerySubject(
                re.compile(".")):
            urn = unicode(subject)
            filename = None
            if (self.resolver.Get(subject, lexicon.AFF4_CATEGORY) ==
                lexicon.AFF4_MEMORY_PHYSICAL):
                filename = "Physical Memory"
            else:
                filename = self.resolver.Get(subject, lexicon.AFF4_STREAM_ORIGINAL_FILENAME)

            if not filename:
                filename = volume.urn.RelativePath(urn)

            size = self.resolver.Get(subject, lexicon.AFF4_STREAM_SIZE)
            if size is None and filename == "Physical Memory":
                with self.resolver.AFF4FactoryOpen(urn) as fd:
                    last_range = fd.GetRanges()[-1]
                    size = last_range.map_offset + last_range.length

            renderer.table_row(size, filename, urn)

    def interesting_streams(self, volume):
        """Returns the interesting URNs and their filenames."""
        urns = {}

        for (subject, _, value) in self.resolver.QueryPredicate(
                lexicon.AFF4_STREAM_ORIGINAL_FILENAME):
            # Normalize the filename for case insensitive filesysyems.
            urn = unicode(subject)
            urns[urn] = unicode(value)

        for (subject, _, value) in self.resolver.QueryPredicate(
                lexicon.AFF4_CATEGORY):
            if value == lexicon.AFF4_MEMORY_PHYSICAL:
                urn = unicode(subject)
                urns[urn] = "Physical Memory"

        # Add metadata files.
        for subject in self.resolver.QuerySubject(
                re.compile(".+(yaml|turtle)")):
                urn = unicode(subject)
                urns[urn] = volume.urn.RelativePath(urn)

        return urns

    def render_short(self, renderer, volume):
        """Render a concise description of the contents of an AFF4 volume."""
        renderer.table_header([
            dict(name="Size", width=15),
            dict(name="Original Name", width=50),
            dict(name="URN", width=150),
        ])

        for urn, filename in self.interesting_streams(volume).iteritems():
            size = self.resolver.Get(urn, lexicon.AFF4_STREAM_SIZE)
            if size is None and filename == "Physical Memory":
                with self.resolver.AFF4FactoryOpen(urn) as fd:
                    last_range = fd.GetRanges()[-1]
                    size = last_range.map_offset + last_range.length

            renderer.table_row(size, filename, urn)

    def render(self, renderer):
        volume_urn = rdfvalue.URN().FromFileName(self.volume_path)
        with zip.ZipFile.NewZipFile(self.resolver, volume_urn) as volume:
            if self.long:
                self.render_long(renderer, volume)
            else:
                self.render_short(renderer, volume)


class AFF4Export(core.DirectoryDumperMixin, plugin.Command):
    """Exports all the streams in an AFF4 Volume."""
    dump_dir_optional = False
    default_dump_dir = None

    BUFFERSIZE = 1024 * 1024

    name = "aff4export"

    @classmethod
    def args(cls, parser):
        super(AFF4Export, cls).args(parser)

        parser.add_argument(
            "--regex", default=".",
            help="Regex of filenames to dump.")

        parser.add_argument(
            "volume", default=None, required=True,
            help="Volume to list.")

    def __init__(self, volume=None, regex=".", **kwargs):
        super(AFF4Export, self).__init__(**kwargs)
        self.volume_path = volume
        self.regex = re.compile(regex)
        self.aff4ls = self.session.plugins.aff4ls()
        self.resolver = self.aff4ls.resolver

    def _sanitize_filename(self, filename):
        filename = filename.replace("\\", "/")
        filename = filename.strip("/")
        result = []
        for x in filename:
            if x == "/":
                result.append("_")
            elif x.isalnum() or x in "_-=.,; ":
                result.append(x)
            else:
                result.append("%" + x.encode("hex"))

        return "".join(result)

    def copy_stream(self, in_fd, out_fd, length=2**64):
        total = 0
        while 1:
            available_to_read = min(length - total, self.BUFFERSIZE)
            data = in_fd.read(available_to_read)
            if not data:
                break

            out_fd.write(data)
            total += len(data)
            self.session.report_progress("Reading %s @ %#x", in_fd.urn, total)

    def copy_map(self, in_fd, out_fd):
        for range in in_fd.GetRanges():
            self.session.logging.info("Range %s", range)
            out_fd.seek(range.map_offset)
            in_fd.seek(range.map_offset)
            self.copy_stream(in_fd, out_fd, range.length)

    def render(self, renderer):
        volume_urn = rdfvalue.URN().FromFileName(self.volume_path)
        with zip.ZipFile.NewZipFile(self.resolver, volume_urn) as volume:
            for urn, filename in self.aff4ls.interesting_streams(volume).items():
                if self.regex.match(filename):
                    # Force the file to be under the dumpdir.
                    filename=self._sanitize_filename(filename)
                    self.session.logging.info("Dumping %s", filename)

                    with renderer.open(directory=self.dump_dir,
                                       filename=filename,
                                       mode="wb") as out_fd:
                        with self.resolver.AFF4FactoryOpen(urn) as in_fd:
                            if isinstance(in_fd, aff4_map.AFF4Map):
                                self.copy_map(in_fd, out_fd)
                            else:
                                self.copy_stream(in_fd, out_fd)

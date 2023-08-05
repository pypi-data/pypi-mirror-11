#!/usr/bin/env python

"""
"""

import os
import tarfile
import tempfile
import unittest

from concrete.util import (
    CommunicationReader,
    CommunicationWriter,
    CommunicationWriterTGZ,
    read_communication_from_file
)
from concrete.validate import validate_communication

class TestCommunicationReader(unittest.TestCase):
    def test_single_file(self):
        filename = u'tests/testdata/simple_1.concrete'
        reader = CommunicationReader(filename)
        (comm1, comm1_filename) = reader.next()
        self.assertTrue(hasattr(comm1, 'sentenceForUUID'))
        self.assertEqual(u'one', comm1.id)
        self.assertEqual(filename, comm1_filename)

    def test_single_gz_file(self):
        filename = u'tests/testdata/simple_1.concrete.gz'
        reader = CommunicationReader(filename)
        (comm1, comm1_filename) = reader.next()
        self.assertTrue(hasattr(comm1, 'sentenceForUUID'))
        self.assertEqual(u'one', comm1.id)
        self.assertEqual(filename, comm1_filename)

    def test_concatenated_file(self):
        filename = u'tests/testdata/simple_concatenated'
        reader = CommunicationReader(filename)
        [comms, filenames] = zip(*[(c, f) for (c, f) in reader])
        for (i, comm_id) in enumerate([u'one', u'two', u'three']):
            self.assertTrue(hasattr(comms[i], 'sentenceForUUID'))
            self.assertEqual(comm_id, comms[i].id)
            self.assertEqual(filename, filenames[i])

    def test_concatenated_gz_file(self):
        filename = u'tests/testdata/simple_concatenated.gz'
        reader = CommunicationReader(filename)
        [comms, filenames] = zip(*[(c, f) for (c, f) in reader])
        for (i, comm_id) in enumerate([u'one', u'two', u'three']):
            self.assertTrue(hasattr(comms[i], 'sentenceForUUID'))
            self.assertEqual(comm_id, comms[i].id)
            self.assertEqual(filename, filenames[i])

    def test_tar_file(self):
        filename = u'tests/testdata/simple.tar'
        reader = CommunicationReader(filename)
        [comms, filenames] = zip(*[(c, f) for (c, f) in reader])
        self.assertTrue(hasattr(comms[0], 'sentenceForUUID'))
        self.assertTrue(hasattr(comms[1], 'sentenceForUUID'))
        self.assertTrue(hasattr(comms[2], 'sentenceForUUID'))
        self.assertEqual(u'one', comms[0].id)
        self.assertEqual(u'two', comms[1].id)
        self.assertEqual(u'three', comms[2].id)
        self.assertEqual(u'simple_1.concrete', filenames[0])
        self.assertEqual(u'simple_2.concrete', filenames[1])
        self.assertEqual(u'simple_3.concrete', filenames[2])

    def test_tar_gz_file(self):
        reader = CommunicationReader("tests/testdata/simple.tar.gz")
        [comms, filenames] = zip(*[(c, f) for (c, f) in reader])
        self.assertTrue(hasattr(comms[0], 'sentenceForUUID'))
        self.assertTrue(hasattr(comms[1], 'sentenceForUUID'))
        self.assertTrue(hasattr(comms[2], 'sentenceForUUID'))
        self.assertEqual(u'one', comms[0].id)
        self.assertEqual(u'two', comms[1].id)
        self.assertEqual(u'three', comms[2].id)
        self.assertEqual(u'simple_1.concrete', filenames[0])
        self.assertEqual(u'simple_2.concrete', filenames[1])
        self.assertEqual(u'simple_3.concrete', filenames[2])

    def test_zip_file(self):
        reader = CommunicationReader("tests/testdata/simple.zip")
        [comms, filenames] = zip(*[(c, f) for (c, f) in reader])
        self.assertTrue(hasattr(comms[0], 'sentenceForUUID'))
        self.assertTrue(hasattr(comms[1], 'sentenceForUUID'))
        self.assertTrue(hasattr(comms[2], 'sentenceForUUID'))
        self.assertEqual(u'one', comms[0].id)
        self.assertEqual(u'two', comms[1].id)
        self.assertEqual(u'three', comms[2].id)
        self.assertEqual(u'simple_1.concrete', filenames[0])
        self.assertEqual(u'simple_2.concrete', filenames[1])
        self.assertEqual(u'simple_3.concrete', filenames[2])

    def test_single_file_no_add_references(self):
        filename = u'tests/testdata/simple_1.concrete'
        reader = CommunicationReader(filename, add_references=False)
        (comm1, comm1_filename) = reader.next()
        self.assertFalse(hasattr(comm1, 'sentenceForUUID'))
        self.assertEqual(u'one', comm1.id)
        self.assertEqual(filename, comm1_filename)

    def test_single_gz_file_no_add_references(self):
        filename = u'tests/testdata/simple_1.concrete.gz'
        reader = CommunicationReader(filename, add_references=False)
        (comm1, comm1_filename) = reader.next()
        self.assertFalse(hasattr(comm1, 'sentenceForUUID'))
        self.assertEqual(u'one', comm1.id)
        self.assertEqual(filename, comm1_filename)

    def test_concatenated_file_no_add_references(self):
        filename = u'tests/testdata/simple_concatenated'
        reader = CommunicationReader(filename, add_references=False)
        [comms, filenames] = zip(*[(c, f) for (c, f) in reader])
        for (i, comm_id) in enumerate([u'one', u'two', u'three']):
            self.assertFalse(hasattr(comms[i], 'sentenceForUUID'))
            self.assertEqual(comm_id, comms[i].id)
            self.assertEqual(filename, filenames[i])

    def test_concatenated_gz_file_no_add_references(self):
        filename = u'tests/testdata/simple_concatenated.gz'
        reader = CommunicationReader(filename, add_references=False)
        [comms, filenames] = zip(*[(c, f) for (c, f) in reader])
        for (i, comm_id) in enumerate([u'one', u'two', u'three']):
            self.assertFalse(hasattr(comms[i], 'sentenceForUUID'))
            self.assertEqual(comm_id, comms[i].id)
            self.assertEqual(filename, filenames[i])

    def test_tar_file_no_add_references(self):
        filename = u'tests/testdata/simple.tar'
        reader = CommunicationReader(filename, add_references=False)
        [comms, filenames] = zip(*[(c, f) for (c, f) in reader])
        self.assertFalse(hasattr(comms[0], 'sentenceForUUID'))
        self.assertFalse(hasattr(comms[1], 'sentenceForUUID'))
        self.assertFalse(hasattr(comms[2], 'sentenceForUUID'))
        self.assertEqual(u'one', comms[0].id)
        self.assertEqual(u'two', comms[1].id)
        self.assertEqual(u'three', comms[2].id)
        self.assertEqual(u'simple_1.concrete', filenames[0])
        self.assertEqual(u'simple_2.concrete', filenames[1])
        self.assertEqual(u'simple_3.concrete', filenames[2])

    def test_tar_gz_file_no_add_references(self):
        reader = CommunicationReader("tests/testdata/simple.tar.gz", add_references=False)
        [comms, filenames] = zip(*[(c, f) for (c, f) in reader])
        self.assertFalse(hasattr(comms[0], 'sentenceForUUID'))
        self.assertFalse(hasattr(comms[1], 'sentenceForUUID'))
        self.assertFalse(hasattr(comms[2], 'sentenceForUUID'))
        self.assertEqual(u'one', comms[0].id)
        self.assertEqual(u'two', comms[1].id)
        self.assertEqual(u'three', comms[2].id)
        self.assertEqual(u'simple_1.concrete', filenames[0])
        self.assertEqual(u'simple_2.concrete', filenames[1])
        self.assertEqual(u'simple_3.concrete', filenames[2])

    def test_zip_file_no_add_references(self):
        reader = CommunicationReader("tests/testdata/simple.zip", add_references=False)
        [comms, filenames] = zip(*[(c, f) for (c, f) in reader])
        self.assertFalse(hasattr(comms[0], 'sentenceForUUID'))
        self.assertFalse(hasattr(comms[1], 'sentenceForUUID'))
        self.assertFalse(hasattr(comms[2], 'sentenceForUUID'))
        self.assertEqual(u'one', comms[0].id)
        self.assertEqual(u'two', comms[1].id)
        self.assertEqual(u'three', comms[2].id)
        self.assertEqual(u'simple_1.concrete', filenames[0])
        self.assertEqual(u'simple_2.concrete', filenames[1])
        self.assertEqual(u'simple_3.concrete', filenames[2])


class TestCommunicationWriter(unittest.TestCase):
    def test_single_file(self):
        comm = read_communication_from_file("tests/testdata/simple_1.concrete")
        writer = CommunicationWriter()
        (file_handle, filename) = tempfile.mkstemp()
        writer.open(filename)
        writer.write(comm)
        writer.close()

        os.remove(filename)

    def test_single_file_ctx_mgr(self):
        comm = read_communication_from_file("tests/testdata/simple_1.concrete")
        (file_handle, filename) = tempfile.mkstemp()
        with CommunicationWriter(filename) as writer:
            writer.write(comm)

        os.remove(filename)


class TestCommunicationWriterTGZ(unittest.TestCase):
    def test_single_file(self):
        comm = read_communication_from_file("tests/testdata/simple_1.concrete")
        writer = CommunicationWriterTGZ()
        (file_handle, filename) = tempfile.mkstemp()
        writer.open(filename)
        writer.write(comm, "simple_1.concrete")
        writer.close()

        self.assertTrue(tarfile.is_tarfile(filename))
        os.remove(filename)

    def test_single_file_ctx_mgr(self):
        comm = read_communication_from_file("tests/testdata/simple_1.concrete")
        (file_handle, filename) = tempfile.mkstemp()
        with CommunicationWriterTGZ(filename) as writer:
            writer.write(comm, "simple_1.concrete")

        self.assertTrue(tarfile.is_tarfile(filename))
        os.remove(filename)


if __name__ == '__main__':
    unittest.main(buffer=True)

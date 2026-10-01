from pathlib import Path
import hashlib
import importlib.util
import struct
import tempfile
import unittest
import zlib

spec = importlib.util.spec_from_file_location('recovery', Path(__file__).resolve().parents[1] / 'tools/recover_resources.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.addCleanup(self.directory.cleanup)
        self.data = b'synthetic test resource'
        packed = zlib.compress(self.data)
        index = b'data/test.bin\0' + struct.pack('<IIIBI', len(packed), len(packed), len(self.data), 1, 0)
        compressed_index = zlib.compress(index)
        header = bytearray(46)
        header[:15] = b'Master of Magic'
        struct.pack_into('<I', header, 30, len(packed))
        struct.pack_into('<I', header, 42, 0x200)
        self.grf = self.root / 'synthetic.grf'
        self.grf.write_bytes(header + packed + struct.pack('<II', len(compressed_index), len(index)) + compressed_index)
        self.recipe = {'name': 'test', 'files': [{'path': 'data/test.bin', 'source': 'data/test.bin', 'sha256': hashlib.sha256(self.data).hexdigest(), 'status': 'verified original path'}]}

    def test_verified_resource_is_written(self):
        result = module.recover(module.Grf(self.grf), self.recipe, self.root / 'output')
        self.assertEqual(result['verified'], 1)
        self.assertEqual((self.root / 'output/data/test.bin').read_bytes(), self.data)

    def test_mismatched_reference_is_not_written(self):
        self.recipe['files'][0]['sha256'] = '0' * 64
        result = module.recover(module.Grf(self.grf), self.recipe, self.root / 'output')
        self.assertEqual(result['verified'], 0)
        self.assertEqual(len(result['unresolved']), 1)
        self.assertFalse((self.root / 'output').exists())

    def test_verify_only_does_not_write(self):
        result = module.recover(module.Grf(self.grf), self.recipe, self.root / 'output', True)
        self.assertEqual(result['verified'], 1)
        self.assertFalse((self.root / 'output').exists())

    def test_path_traversal_is_rejected(self):
        self.recipe['files'][0]['path'] = '../outside.bin'
        with self.assertRaises(ValueError):
            module.recover(module.Grf(self.grf), self.recipe, self.root / 'output')

if __name__ == '__main__':
    unittest.main()

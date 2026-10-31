"""Offline screenshot reader and brand assets are complete, attributed and uncorrupted."""
from pathlib import Path
import unittest,json,hashlib,gzip
ROOT=Path(__file__).resolve().parents[1]
class OfflineAssetTests(unittest.TestCase):
 def test_vendor_checksums_and_local_reader_variants(self):
  data=json.loads((ROOT/'assets/vendor-sources.json').read_text())
  for name,digest in data['files'].items():self.assertEqual(hashlib.sha256((ROOT/'assets'/name).read_bytes()).hexdigest(),digest,name)
  for lang in ['eng','ara']:self.assertGreater(len(gzip.decompress((ROOT/f'assets/screenshot-reader/{lang}.traineddata.gz').read_bytes())),100000)
  for variant in ['lstm','simd-lstm','relaxedsimd-lstm']:self.assertTrue((ROOT/f'assets/screenshot-reader/tesseract-core-{variant}.wasm.js').is_file())
  for platform in ['X','Facebook','Instagram','Telegram','Threads']:self.assertTrue(data['logos'][platform]['source'].startswith('https://'))
if __name__=='__main__':unittest.main()

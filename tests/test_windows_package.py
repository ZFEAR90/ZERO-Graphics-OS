from pathlib import Path
import importlib.util,unittest,tempfile,zipfile,json
ROOT=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('package_builder',ROOT/'tools/build_windows_package.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
class PackageTests(unittest.TestCase):
 def test_connected_launcher_and_exact_source_files(self):
  with tempfile.TemporaryDirectory() as folder:
   target=builder.build(Path(folder)/'test.zip')
   with zipfile.ZipFile(target) as z:
    self.assertIsNone(z.testzip());manifest=json.loads(z.read('Main_roll_Beta_2.7.8/package_manifest.json'));self.assertEqual(manifest['mode'],'connected URL importer')
    for name in builder.FILES:self.assertEqual(z.read('Main_roll_Beta_2.7.8/'+name),(ROOT/name).read_bytes())
    self.assertIn(b'START_ZE_OS.bat',z.read('Main_roll_Beta_2.7.8/TEST_MAIN_ROLL.bat'));self.assertFalse(any('.venv' in name or 'STARTUP_LOG' in name for name in z.namelist()))
if __name__=='__main__':unittest.main()

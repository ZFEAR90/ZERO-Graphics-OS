"""Build the complete connected-importer Windows ZIP; never include local environments/logs."""
from pathlib import Path
import zipfile,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
FILES=['TEST_MAIN_ROLL.bat','START_ZE_OS.bat','OFFLINE_MAIN_ROLL.bat','INSTALL_CAPTURE_BROWSER.bat','README_TEST_WINDOWS.txt','ZE_OS_Mouwajaha_V07.html','ze_local_importer.py','requirements.txt']
def build(target):
 target=Path(target);target.parent.mkdir(parents=True,exist_ok=True);manifest={'version':'0.7-beta2.7.8','default_launcher':'TEST_MAIN_ROLL.bat','mode':'connected URL importer','files':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in FILES}}
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name in FILES:z.write(ROOT/name,arcname='Main_roll_Beta_2.7.8/'+name)
  z.writestr('Main_roll_Beta_2.7.8/package_manifest.json',json.dumps(manifest,indent=2)+'\n')
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  for name in FILES:assert hashlib.sha256(z.read('Main_roll_Beta_2.7.8/'+name)).hexdigest()==manifest['files'][name]
 return target
if __name__=='__main__':print(build(sys.argv[1] if len(sys.argv)>1 else ROOT/'downloads/Main_roll_test.zip'))

"""Python startup contract exercised with a real process, including nondefault port."""
from pathlib import Path
import unittest,subprocess,os,re,urllib.request,json,tempfile,threading
from unittest.mock import patch
from browser_support import helper,ROOT
class LauncherTests(unittest.TestCase):
 def test_real_startup_and_health_log(self):
  with tempfile.TemporaryDirectory() as folder:
   log=Path(folder)/'startup.log';env=os.environ.copy();env['ZE_OS_PORT']='0'
   process=subprocess.Popen([os.sys.executable,str(ROOT/'ze_local_importer.py'),'--no-browser','--startup-log',str(log)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,env=env)
   try:
    line=process.stdout.readline();match=re.search(r'(http://127\.0\.0\.1:\d+)/ZE_OS',line);self.assertIsNotNone(match,line);base=match[1]
    with urllib.request.urlopen(base+'/api/health',timeout=3) as response:self.assertEqual(json.load(response),{'service':'ze-os-importer','version':'0.7-beta2.7.8'})
    with urllib.request.urlopen(base+'/ZE_OS_Mouwajaha_V07.html',timeout=3) as response:self.assertIn(b'zeUniversalWorkspace',response.read())
    self.assertIn('Main roll with URL importing',log.read_text())
   finally:process.terminate();process.wait(timeout=5);process.stdout.close()
 def test_same_instance_reopens_without_port_conflict(self):
  server=helper.create_editor_server(0);threading.Thread(target=server.serve_forever,daemon=True).start()
  try:
   with patch('webbrowser.open') as opened:self.assertEqual(helper.run_editor(server.server_port),0);opened.assert_called_once()
  finally:server.shutdown();server.server_close()
 def test_missing_pip_can_be_repaired_without_recreating_environment(self):
  with tempfile.TemporaryDirectory() as folder:
   target=Path(folder)/'local-env'
   subprocess.run([os.sys.executable,'-m','venv','--without-pip',str(target)],check=True,capture_output=True)
   python=target/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
   marker=target/'existing-user-file.txt';marker.write_text('preserve')
   self.assertNotEqual(subprocess.run([str(python),'-m','pip','--version'],capture_output=True).returncode,0)
   subprocess.run([str(python),'-m','ensurepip','--upgrade'],check=True,capture_output=True)
   subprocess.run([str(python),'-m','pip','--version'],check=True,capture_output=True)
   self.assertEqual(marker.read_text(),'preserve')
  start=(ROOT/'START_ZE_OS.bat').read_text()
  self.assertLess(start.index('-m ensurepip --upgrade'),start.index('-m pip install -r requirements.txt'))
  self.assertIn('if errorlevel 1 goto pip_missing',start)
 def test_launcher_modes_are_explicit(self):
  self.assertIn('START_ZE_OS.bat',(ROOT/'TEST_MAIN_ROLL.bat').read_text());self.assertNotIn('start ""',(ROOT/'TEST_MAIN_ROLL.bat').read_text())
  start=(ROOT/'START_ZE_OS.bat').read_text();self.assertIn('--startup-log STARTUP_LOG.txt',start);self.assertIn('sys.version_info >= (3,10)',start);self.assertNotIn('-m playwright install chromium',start)
  self.assertIn('-m playwright install chromium',(ROOT/'INSTALL_CAPTURE_BROWSER.bat').read_text());self.assertIn('OFFLINE',(ROOT/'OFFLINE_MAIN_ROLL.bat').read_text())
if __name__=='__main__':unittest.main()

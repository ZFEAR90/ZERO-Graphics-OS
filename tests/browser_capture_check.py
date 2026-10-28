from pathlib import Path
import importlib.util
from unittest.mock import patch,MagicMock
from playwright.sync_api import sync_playwright
spec=importlib.util.spec_from_file_location('helper',Path(__file__).resolve().parents[1]/'ze_local_importer.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
url='https://www.facebook.com/share/p/1GVmqHPmx5/'
with sync_playwright() as p:
 for scenario in ['public','denied','login']:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  original_new_page=browser.new_page
  def page_factory(**kw):
   page=original_new_page(**kw)
   if scenario=='login':
    original_goto=page.goto
    page.goto=lambda url,**options:original_goto('https://www.facebook.com/login',**options)
   def route_handler(route):
    if scenario=='public':
     route.fulfill(status=200,content_type='text/html',body='<article role="article" style="width:600px;min-height:350px;background:white"><h2><a>Public Author</a></h2><p>Actual fixture post content</p></article>')
    else:route.fulfill(status=400 if scenario=='denied' else 200,content_type='text/html',body='<h1>Sign in</h1>')
   page.route('**/*',route_handler);return page
  ctx=MagicMock();ctx.__enter__.return_value=p
  with patch('playwright.sync_api.sync_playwright',return_value=ctx),patch.object(m,'launch_capture_browser',return_value=browser),patch.object(browser,'new_page',side_effect=page_factory):
   result=m.screenshot_public_post(url)
  if scenario=='public':
   assert result['screenshot_data'].startswith('data:image/png;base64,');assert result['name']=='Public Author';print('PUBLIC: actual browser captured post and author')
  elif scenario=='denied':assert 'HTTP 400' in result['capture_error'];print('DENIED: browser rejection reported')
  else:assert 'login' in result['capture_error'],result;print('LOGIN: login page rejected as a post')

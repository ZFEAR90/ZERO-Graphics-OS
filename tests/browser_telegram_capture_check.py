"""Actual Chromium Telegram widget: large channel avatar must never become post media."""
from pathlib import Path
import importlib.util,base64
from unittest.mock import patch,MagicMock
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('telegram_capture_helper',root/'ze_local_importer.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
with sync_playwright() as p:
 for with_photo in [False,True]:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);new_page=browser.new_page
  body='Original Telegram text '*220
  def factory(**kw):
   page=new_page(**kw)
   def route(r):
    if r.request.url.endswith('.png'):r.fulfill(content_type='image/png',body=(root/'tests/fixtures/portrait.png').read_bytes())
    else:
     photo='<a class="tgme_widget_message_photo_wrap" style="display:block;width:300px;height:180px;background-image:url(https://cdn-telegram.org/post.png)"></a>' if with_photo else ''
     r.fulfill(content_type='text/html',body='<div class="tgme_widget_message" style="width:600px;min-height:300px;background:white"><a class="tgme_widget_message_user_photo"><img src="https://cdn-telegram.org/avatar.png" width="100"></a><a class="tgme_widget_message_owner_name">Original Channel</a><div class="tgme_widget_message_text">'+body+'<br>Last line</div>'+photo+'</div>')
   page.route('**/*',route);return page
  ctx=MagicMock();ctx.__enter__.return_value=p
  with patch('playwright.sync_api.sync_playwright',return_value=ctx),patch.object(helper,'launch_capture_browser',return_value=browser),patch.object(browser,'new_page',side_effect=factory),patch.object(helper,'image_data',side_effect=lambda url:'data:image/png;base64,'+base64.b64encode(url.encode()).decode()):
   result=helper.screenshot_public_post('https://t.me/alichoeib1970/19404')
  assert result.get('screenshot_data'),result
  assert result['text']==body+'\nLast line',result.get('text')
  assert result['name']=='Original Channel'
  assert len(result['attachments'])==int(with_photo),result['attachments']
  assert all(item['data_url']!=result['avatar_data'] for item in result['attachments'])
 print('Actual Telegram widget capture: full original text and profile retained; avatar excluded from post media; actual photo included: passed')

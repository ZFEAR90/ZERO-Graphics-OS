"""Real local API import plus disconnected-helper preservation; no live scraping claim."""
from browser_support import scene,helper,ROOT
import base64
photo="data:image/png;base64,"+base64.b64encode((ROOT/"tests/fixtures/photo.png").read_bytes()).decode()
from unittest.mock import patch
with patch.object(helper,'public_url',side_effect=lambda url,patterns:url),patch.object(helper,'fetch_metadata',return_value={'platform':'X','name':'Fixture URL author','handle':'fixture','text':'Actual deterministic importer fixture text','status':'partial','attachments':[{'type':'image','data_url':photo}]}),patch.object(helper,'screenshot_public_post',return_value={'capture_error':'Fixture capture not requested'}):
 with scene('importer-connection') as s:
  p=s.page;p.locator('#linkImport').evaluate('e=>e.open=true');p.locator('#postUrl').fill('https://x.com/fixture/status/123456789');p.locator('#importPost').click();p.wait_for_function("zePost.active&&document.getElementById('displayname').value==='Fixture URL author'")
  assert p.locator('#postBody').input_value()=='Actual deterministic importer fixture text'
  assert p.evaluate("zePost.items.length===1&&zeVisualItems()[0].type==='image'&&zePostRollText()===''")
  assert p.locator('#postMediaFit').input_value()=='fit' and p.locator('#postTextPlacement').input_value()=='bullet'
  assert p.locator('#bullets').input_value()=='Actual deterministic importer fixture text'
  assert '0.7-beta2.7.8' in p.locator('#importerConnection').inner_text()
  before=p.evaluate('({text:document.getElementById("postBody").value,name:document.getElementById("displayname").value})')
  p.route('**/api/health',lambda route:route.abort());p.locator('#importPost').click();p.wait_for_function("!document.getElementById('importPost').disabled")
  assert 'STARTUP_LOG.txt' in p.locator('#importStatus').inner_text()
  assert before==p.evaluate('({text:document.getElementById("postBody").value,name:document.getElementById("displayname").value})')
  print('Actual local importer connection and URL request populate editor; disconnected helper preserves content and exposes startup guidance: passed')

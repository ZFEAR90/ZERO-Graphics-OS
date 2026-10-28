from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
import threading,json
root=str(Path(__file__).resolve().parents[1])
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=root))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1920,'height':1080});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html')
  page.wait_for_function('assets.source && assets.avatar && state.stvLoaded')
  page.locator('.control-panel').evaluate_all('(panels)=>panels.forEach(panel=>panel.open=true)')
  print('FONT',page.evaluate('({loaded:state.stvLoaded,regular:document.fonts.check("400 21px ZEOSSTV"),bold:document.fonts.check("700 21px ZEOSSTV")})'))
  for flipped in [False,True]:
   for text in ['xpos','A much longer source display name','قناة الميادين الإخبارية','A'*200]:
    page.locator('#displayname').fill(text);page.evaluate('(v)=>setFlipped(v)',flipped);page.evaluate('setT(4)')
    l=page.evaluate('headerLayout(c)');a=l['avatar'];n=l['name'];gap=(a['x']-(n['x']+n['w'])) if flipped else (n['x']-(a['x']+a['w']))
    assert abs(gap-6)<.01,(gap,l)
    assert n['x']>=42 and n['x']+n['w']<=474
  print('LABELS 8 long/short/Arabic/flip cases passed')
  page.locator('#displayname').fill('Al Mayadeen News');page.evaluate('setFlipped(false)')
  for mode in ['enhanced','reference']:
   page.locator('#mode'+mode.title()).click()
   for t in [0,.32,.8,1.2,1.6,2.12,4]:
    page.evaluate('(t)=>setT(t)',t)
    if mode=='enhanced':page.locator('#canvas').screenshot(path=f'/tmp/ze-beta-{t}.png')
  page.locator('#modeEnhanced').click();page.evaluate('setT(4);setFlipped(true)');page.locator('#canvas').screenshot(path='/tmp/ze-beta-flipped.png')
  page.locator('#showBullets').uncheck();assert page.evaluate('getBBox("bullet").w')==0
  assert abs(page.evaluate('getBBox("source").x+getBBox("source").w/2')-480)<.01
  page.locator('#canvas').screenshot(path='/tmp/ze-beta-solo.png');page.locator('#showBullets').check()
  page.locator('[data-view="compare"]').click();page.evaluate('setT(1.6)');page.wait_for_timeout(200)
  assert abs(page.evaluate('cmp.currentTime-state.t'))<.001
  page.locator('[data-view="rebuild"]').click()
  page.evaluate('window.priorImport={source:assets.source,avatar:assets.avatar,platform:assets.platform,name:document.getElementById("displayname").value,account:document.getElementById("account").value}')
  page.locator('#postUrl').fill('https://www.facebook.com/share/p/1Cuq9SFPGz/')
  page.route('**/api/health',lambda route:route.abort('failed'))
  page.locator('#importPost').click()
  page.wait_for_function('!document.getElementById("importPost").disabled')
  assert 'not reachable' in page.locator('#importStatus').inner_text()
  assert page.evaluate('assets.source===priorImport.source && assets.avatar===priorImport.avatar && assets.platform===priorImport.platform && document.getElementById("displayname").value===priorImport.name && document.getElementById("account").value===priorImport.account')
  page.locator('#canvas').screenshot(path='/tmp/ze-beta2-failed-import.png')
  print('Disconnected importer preserves all scene assets and labels')
  page.unroute('**/api/health')
  page.route('**/api/health',lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps({'service':'ze-os-importer','version':'0.7-beta2'})))
  page.route('**/api/post?*',lambda route:route.fulfill(status=422,content_type='application/json',body=json.dumps({'error':'This post requires login'})))
  page.locator('#importPost').click();page.wait_for_function('!document.getElementById("importPost").disabled')
  assert 'requires login' in page.locator('#importStatus').inner_text()
  assert page.evaluate('assets.source===priorImport.source && assets.avatar===priorImport.avatar')
  print('Platform denial preserves scene and displays actual error')
  page.unroute('**/api/post?*')
  image=page.evaluate('assets.avatar.src')
  payload={'platform':'X','name':'Imported Author','handle':'real_author','text':'Public post content from importer fixture','avatar_data':image,'media_data':image,'status':'partial'}
  page.route('**/api/post?*',lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps(payload)))
  page.locator('#postUrl').fill('https://x.com/real_author/status/123456789');page.locator('#importPost').click()
  page.wait_for_function('document.getElementById("displayname").value==="Imported Author" && assets.avatar && assets.source')
  assert page.evaluate('assets.sourceBottom===null && !!assets.platform')
  assert page.locator('#account').input_value()=='@real_author'
  print('IMPORT UI name/profile/logo/post replacement passed with fixture; live service separate')
  page.evaluate('setT(4)');page.locator('#canvas').screenshot(path='/tmp/ze-beta-imported.png')
  assert not errors,errors
  print('BROWSER ERRORS',errors);browser.close()
finally:server.shutdown();server.server_close()

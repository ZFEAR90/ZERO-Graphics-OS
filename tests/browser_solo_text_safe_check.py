"""Solo post text uses a safe scroll aperture without shrinking its outer frame."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading,json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1920,'height':1080});errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('state.stvLoaded && assets.source');page.locator('#showBullets').uncheck()
  texts=['نص عربي طويل للاختبار يجب أن يبقى كاملاً فوق منطقة الخبر العاجل مع استمرار التمرير داخل الرول. ','A readable English article should scroll above the selected lower-third boundary without resizing its frame. ']
  for text in texts:
   page.evaluate(r'''async(text)=>zeCommitPost(await zePreparePost({text:(text.repeat(4)+'\n\n').repeat(7),attachments:[]}))''',text)
   assert page.evaluate('zeSafeRollText() && !zeReferenceMediaFrame()')
   for protection in [False,True]:
    for boundary in [847,760]:
     for movement in [0,80]:
      result=page.evaluate('''(v)=>{document.getElementById('protectLowerThird').checked=v.protection;document.getElementById('breakingNewsTop').value=v.boundary;document.getElementById('compositionY').value=v.movement;const boxes=zeSafeLayout(),good=zeDrawPostDocument;let changed=0,outside=0;for(const t of [2.04,2.2,2.4,2.8,5,25,49.96]){setT(t);const a=c.getImageData(0,0,1920,1080).data;zeDrawPostDocument=()=>{};draw();const b=c.getImageData(0,0,1920,1080).data;zeDrawPostDocument=good;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3]){changed++;if(Math.floor(i/4/1920)>=zeBroadcastBounds().bottom*2)outside++}}draw();return {changed,outside,box:getBBox('source'),unchanged:JSON.stringify(boxes)===JSON.stringify(zeSafeLayout())}}''',dict(protection=protection,boundary=boundary,movement=movement))
      assert result['changed']>0 and result['outside']==0 and result['unchanged'],result
      assert result['box']['w']==760,result
   print(text[:18],'solo frame retained; painted text safe across custom boundaries, movement, protection and entrance/scroll/end: passed',flush=True)
  page.evaluate('document.getElementById("protectLowerThird").checked=false;document.getElementById("breakingNewsTop").value=847;document.getElementById("compositionY").value=0;setT(49.96)')
  metrics=page.evaluate('''(()=>{let target=null;const old=zeDrawPostDocument;zeDrawPostDocument=(c,x,y,w,h,t)=>{target={x,y,w,h,doc:zePostDocument().height};old(c,x,y,w,h,t)};draw();zeDrawPostDocument=old;return {target,box:getBBox('source'),safe:zeBroadcastBounds()}})()''')
  assert metrics['box']['y']+metrics['box']['h']>metrics['safe']['top'] and metrics['target']['y']+metrics['target']['h']<=metrics['safe']['bottom']-1.99,metrics
  with page.expect_download() as output:page.locator('#saveJson').click()
  output.value.save_as('/tmp/ze-beta273-text.json');assert json.loads(Path('/tmp/ze-beta273-text.json').read_text())['safeArea']['soloRollTextAlwaysProtected']
  assert not errors and not page.evaluate('state.renderError'),errors;browser.close()
finally:server.shutdown();server.server_close()

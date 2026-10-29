"""Beta 2.7.8: capacity grouping, immutable Arabic, masks, active clips and workspace."""
from pathlib import Path
from http.server import ThreadingHTTPServer
import importlib.util,threading,json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('helper',root/'ze_local_importer.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
class Handler(helper.Handler):
 def do_GET(self):
  if self.path.startswith('/fixtures/'):return self._send_media(root/'tests/fixtures'/Path(self.path).name)
  super().do_GET()
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1600,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('state.stvLoaded && assets.source')
  assert page.evaluate("typeof zeUniversalWorkspace==='function'") and page.locator('.sidebar.right').count()==0
  assert page.locator('#renderVideo').is_visible() and page.locator('#mainDuration').count()==1
  page.locator('#bullets').fill('فقرة قصيرة\n\nفقرة أخرى');assert page.evaluate('zeParagraphSchedule().rows.length')==1
  page.evaluate("document.getElementById('bulletSplitMode').value='blank';zeUpdateParagraphEditor()");assert page.evaluate('zeParagraphSchedule().rows.length')==2
  page.evaluate("zeParagraphModel.items[0].manual=7;document.getElementById('bullets').value+=' معدلة';zeUpdateParagraphEditor()");assert page.evaluate('zeParagraphModel.items[0].manual')==7
  page.evaluate("document.getElementById('bulletSplitMode').value='auto';document.getElementById('bullets').value='هذا نص طويل لاختبار قياس السعة الفعلية للوحة النص وحماية منطقة الأخبار. '.repeat(100);zeUpdateParagraphEditor()")
  assert page.evaluate('zeParagraphSchedule().rows.length')>3
  assert page.evaluate('zeParagraphSchedule().rows.every(r=>r.lineCount<=Math.floor((zeBulletTextBox().h-zeBulletTextBox().baseline-zeBulletTextBox().font*.65-3)/zeBulletTextBox().lineHeight)+1)')
  page.locator('#bullets').fill('تحرير مستقل');page.evaluate("zePost.bulletLinked=true;zePost.lastBulletCopy='تحرير مستقل';document.getElementById('postTextPlacement').value='roll';zePlacementChanged()");assert page.locator('#bullets').input_value()=='تحرير مستقل'
  for flip in [False,True]:
   for protect in [False,True]:
    g=page.evaluate('''v=>{document.getElementById('protectLowerThird').checked=v.protect;setFlipped(v.flip);const b=zeVisibleBounds('bullet',getBBox('bullet')),h=zeHeaderPaintBounds(getBBox('identity'));setT(5);return {gap:b.y-h.y-h.h,h,b,safe:zeBroadcastBounds()}}''',dict(flip=flip,protect=protect))
    assert abs(g['gap']-24)<.01,g
    assert g['h']['y']>=(34 if g['h']['x']>=g['safe']['x']+114 else g['safe']['y'])-.01,g
  print('Capacity pagination, Auto/blank grouping, preserved manual holds/bullets, painted header gap and corner clearance: passed',flush=True)
  arabic=('هذا نص عربي طويل لاختبار التبرير الآمن والحفاظ على اتصال الحروف داخل الإطار. '*35).rstrip()+'\nالسطر الأخير'
  page.locator('#useWholePost').click();assert page.locator('#showBullets').is_checked();page.locator('#showBullets').uncheck();page.evaluate('''async text=>{zeCommitPost(await zePreparePost({text,attachments:[{type:'image',url:'/fixtures/portrait.png'}]}));setT(5)}''',arabic)
  assert page.evaluate("document.getElementById('postScrollMode').value")=='together'
  assert page.evaluate("document.getElementById('postBody').value")==arabic
  result=page.evaluate('''()=>{const d=zeSocialTextDocument(200);c.save();const line=d.lines.find(l=>!l.final&&l.direction==='rtl');c.font=line.style;const prepared=justifyLine(c,line.text,360,'kashida',1),last=d.lines.at(-1),natural=justifyLine(c,last.text,360,'none',1);c.restore();return {width:prepared.total,kashida:prepared.words.join('').includes('ـ'),last:last.final,natural:natural.total}}''')
  assert abs(result['width']-360)<1 and result['kashida'] and result['last'] and result['natural']<360,result
  movement=page.evaluate('''()=>{let seen=[];const oldT=zeDrawSocialText,oldM=zeDrawPostMediaRegion;zeDrawSocialText=(ctx,b)=>seen.push({kind:'text',y:b.y});zeDrawPostMediaRegion=(ctx,b)=>seen.push({kind:'media',y:b.y});for(const t of [7,20])zeDrawSocialPost(c,0,100,600,250,t);zeDrawSocialText=oldT;zeDrawPostMediaRegion=oldM;return seen}''')
  assert abs((movement[2]['y']-movement[0]['y'])-(movement[3]['y']-movement[1]['y']))<.001 and movement[2]['y']<movement[0]['y'],movement
  page.locator('#showBullets').check();assert page.evaluate("getBBox('bullet').w")>0;page.locator('#showBullets').uncheck()
  page.evaluate("setT(5)");page.locator('#canvas').screenshot(path='/tmp/beta278-whole.png')
  assert page.locator('#postBody').input_value()==arabic
  account=page.evaluate("""()=>{const saved={scale:state.layers.source.scale,avatar:val('avatarScale'),label:val('labelScale')},checks=[];for(const scale of [.3,1]){state.layers.source.scale=scale;document.getElementById('avatarScale').value=250;document.getElementById('labelScale').value=250;const source=getBBox('source'),head=getBBox('identity'),local=headerLayout(c),k=head.w/R.identity.w;checks.push(['avatar','name','handle'].every(n=>{const a=local[n],b={x:head.x+(a.x-R.identity.x)*k,y:head.y+(a.y-R.identity.y)*k,w:a.w*k,h:a.h*k};return b.x>=source.x&&b.y>=source.y&&b.x+b.w<=source.x+source.w+.01&&b.y+b.h<=source.y+source.h+.01}))}state.layers.source.scale=saved.scale;document.getElementById('avatarScale').value=saved.avatar;document.getElementById('labelScale').value=saved.label;return checks}""")
  assert all(account),account
  print('Arabic kashida/unaltered source/natural final line, Whole shared movement, independent bullet visibility: passed',flush=True)
  # Mask coverage and unmirrored pixels at the middle of a transition, for both directions.
  masks=page.evaluate('''()=>{const make=(left,right)=>{const a=document.createElement('canvas');a.width=100;a.height=100;const x=a.getContext('2d');x.fillStyle=left;x.fillRect(0,0,50,100);x.fillStyle=right;x.fillRect(50,0,50,100);return {type:'image',el:a,width:100,height:100,enabled:true}},items=[make('red','blue'),make('green','yellow')],out=document.createElement('canvas');out.width=out.height=100;const x=out.getContext('2d'),results=[];for(const flip of [false,true]){setFlipped(flip);const slot=(timeline(DURATION)-val('sourceTiming')-1.88)/2,t=slot+.4;const seq=zeMediaSequence(t,items);x.clearRect(0,0,100,100);zeDrawPostMediaRegion(x,{x:0,y:0,w:100,h:100},t+1.88,items);const data=x.getImageData(5,5,90,90).data;results.push({seq:seq.layers.map(l=>({weight:l.weight,time:l.time})),opaque:Array.from(data).filter((_,i)=>i%4===3).every(v=>v===255),left:Array.from(x.getImageData(10,50,1,1).data),right:Array.from(x.getImageData(90,50,1,1).data)});}return results}''')
  assert all(r['opaque'] and abs(sum(l['weight'] for l in r['seq'])-1)<1e-8 and abs(r['seq'][1]['time']-.4)<.001 for r in masks),masks
  assert masks[0]['left'][:3]==[0,128,0] and masks[0]['right'][:3]==[0,0,255],masks
  assert masks[1]['left'][:3]==[255,0,0] and masks[1]['right'][:3]==[255,255,0],masks
  print('Complementary masks cover every pixel; flip reverses wipe without mirroring; incoming time/weights: passed',flush=True)
  page.evaluate('''async()=>{zeCommitPost(await zePreparePost({text:'Test video sequence',attachments:[{type:'video',url:'/fixtures/portrait.mp4'},{type:'video',url:'/fixtures/landscape.mp4'}]}));document.getElementById('postScrollMode').value='fixed';setT(5)}''');page.wait_for_function('zePost.items.every(i=>i.el.readyState>=2&&!i.el.seeking)')
  page.evaluate('setT(2.5);state.playing=true');page.wait_for_timeout(200);assert page.evaluate('!zePost.items[0].el.paused && zePost.items[1].el.paused');page.evaluate('state.playing=false;setT(40)');page.wait_for_function('zePost.items.every(i=>!i.el.seeking)');page.evaluate('state.playing=true;zePost.items[1].endBehavior="loop"');page.wait_for_timeout(200);assert page.evaluate('zePost.items[0].el.paused && !zePost.items[1].el.paused')
  page.evaluate('state.playing=false;setT(50)');page.wait_for_timeout(100)
  assert page.evaluate("(()=>{const i=zePost.items[1];i.endBehavior='hold';const hold=zeMediaPlaybackTarget(i,100);i.endBehavior='loop';const loop=zeMediaPlaybackTarget(i,100);return !hold.canPlay&&hold.target<i.el.duration&&loop.canPlay&&loop.target<i.el.duration})()")
  assert page.evaluate("zePost.items.every(i=>!!zePostFrame(i))")
  page.evaluate("document.getElementById('postContentMode').value='text';draw()");s=page.evaluate("getBBox('source')");assert abs(s['x']+s['w']/2-480)<.01,s
  print('Only active video plays, Hold/Loop local timing, cached decoded frames, centered text-only roll: passed',flush=True)
  page.evaluate("document.querySelector('[data-panel=postmedia]').open=true;document.getElementById('postContentMode').value='all';zeRefreshMediaList();draw()")
  page.locator('#postAudio').check();page.wait_for_function('zePost.items.every(i=>i.gain)')
  page.evaluate("setT(1.88+(timeline(DURATION)-val('sourceTiming')-1.88)/2+.4)");page.wait_for_timeout(100)
  gains=page.evaluate('zePost.items.map(i=>i.gain.gain.value)');assert all(abs(g-.5)<.01 for g in gains),gains
  page.locator('#postVideos').uncheck();page.wait_for_timeout(100);assert page.evaluate('zePost.items.every(i=>i.gain.gain.value===0)')
  page.locator('#audioWhenHidden').check();page.wait_for_timeout(100);assert page.evaluate('zePost.items.every(i=>Math.abs(i.gain.gain.value-.5)<.01)')
  page.locator('#audioWhenHidden').uncheck();page.locator('#postVideos').check();page.locator('#postAudio').uncheck()
  print('Audio weights crossfade; hidden video is silent unless explicitly enabled: passed',flush=True)
  page.locator('#useMainRoll').click();page.evaluate("document.getElementById('protectLowerThird').checked=false;document.getElementById('compositionY').value=-40;setT(5);selectLayer('source')")
  before=page.evaluate('zeLayoutSnapshot()');b=page.evaluate("getBBox('source')");page.locator('#canvas').scroll_into_view_if_needed();r=page.locator('#canvas').bounding_box();x=r['x']+(b['x']+b['w']/2)/960*r['width'];y=r['y']+(b['y']+b['h']/2)/540*r['height'];page.mouse.move(x,y);page.mouse.down();page.mouse.move(x-15,y-10,steps=10);page.mouse.up();after=page.evaluate('zeLayoutSnapshot()');assert before!=after
  page.keyboard.press('Control+z');assert page.evaluate('zeLayoutSnapshot()')==before
  page.keyboard.press('Control+Shift+z');assert page.evaluate('zeLayoutSnapshot()')==after
  assert 'restored' in page.locator('#historyStatus').inner_text().lower()
  print('Real drag, one-step Ctrl+Z and Ctrl+Shift+Z, visible movement feedback: passed',flush=True)
  page.locator('#mainTab').click();page.locator('#mainDuration').fill('50');page.locator('#mainDuration').press('Tab');assert page.evaluate('DURATION')==50
  with page.expect_download() as project:page.locator('#saveJson').click()
  project.value.save_as('/tmp/ze-beta278-project.json');saved=json.loads(Path('/tmp/ze-beta278-project.json').read_text());assert saved['version']=='0.7-beta2.7.8' and saved['bulletSplitMode']=='auto' and saved['postJustifyMode']=='kashida' and saved['mediaSequence']['presentation']=='sequence' and saved['postMedia']['audioWhenHidden'] is False
  page.set_viewport_size({'width':780,'height':1000});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert page.locator('#canvas').bounding_box()['y']<page.locator('.sidebar').bounding_box()['y']
  assert not errors and not page.evaluate('state.renderError'),errors
  print('Main timing/Render control, narrow preview-first workspace, zero browser errors: passed',flush=True);browser.close()
finally:server.shutdown();server.server_close()

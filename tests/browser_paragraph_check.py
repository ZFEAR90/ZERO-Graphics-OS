from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading,json,subprocess,base64,io
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1920,'height':1080});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('state.stvLoaded && assets.source');page.evaluate("document.getElementById('bulletSplitMode').value='blank'");page.wait_for_function('zeParagraphModel.ready')
  page.locator('.editor-tab-panel').evaluate_all('(els)=>els.forEach(el=>el.hidden=false)');page.locator('.paragraph-controls').evaluate('(el)=>el.open=true');assert page.evaluate('DURATION')==50;assert page.locator('#scrubber').get_attribute('max')=='50'
  page.locator('#bullets').fill('نص قصير\n\n'+'هذه فقرة أطول لاختبار حساب وقت القراءة بشكل تلقائي ' * 5)
  plan=page.evaluate('zeParagraphSchedule()');assert abs(plan['end']-50)<.001;assert plan['rows'][1]['estimate']>plan['rows'][0]['estimate'];assert plan['rows'][1]['hold']>plan['rows'][0]['hold'];assert len(plan['rows'])==2
  hold=page.get_by_role('spinbutton',name='Hold seconds for paragraph 1');hold.fill('4.5');hold.press('Tab');assert page.evaluate('zeParagraphSchedule().rows[0].hold')==4.5
  assert not page.get_by_role('checkbox',name='Automatic hold for paragraph 1').is_checked()
  page.locator('#videoDuration').fill('35');page.locator('#videoDuration').press('Tab');assert page.evaluate('zeParagraphSchedule().rows[0].hold')==4.5;assert abs(page.evaluate('zeParagraphSchedule().end')-35)<.001
  page.locator('#bullets').fill('نص قصير تم تعديله\n\n'+'هذه فقرة أطول لاختبار حساب وقت القراءة بشكل تلقائي ' * 5);assert page.evaluate('zeParagraphSchedule().rows[0].hold')==4.5
  # Preserve records when reordering paragraphs and treat duplicates independently.
  page.locator('#bullets').fill('ألف\n\nباء\n\nألف');page.get_by_role('spinbutton',name='Hold seconds for paragraph 2').fill('6');page.get_by_role('spinbutton',name='Hold seconds for paragraph 2').press('Tab');page.locator('#bullets').fill('باء\n\nألف\n\nألف');assert page.evaluate('zeParagraphSchedule().rows[0].hold')==6
  page.locator('#videoDuration').fill('5');page.locator('#videoDuration').press('Tab');assert page.evaluate('zeParagraphSchedule().overflow')>0;assert page.locator('#recordFull').is_disabled();assert 'longer' in page.locator('#paragraphTimingStatus').inner_text()
  page.locator('#fitParagraphVideo').click();assert page.evaluate('zeParagraphSchedule().overflow')<.001
  page.locator('#autoParagraphs').click();assert page.evaluate('zeParagraphModel.items.every(r=>r.manual===null)')
  # Hold durations use wall-clock seconds, even when motion speed is adjusted.
  page.evaluate("zeParagraphModel.items[0].manual=4.5;state.speed=1.5;document.getElementById('speed').value=1.5;zeParagraphModel.cache=null;zeUpdateParagraphEditor()")
  plan=page.evaluate('zeParagraphSchedule()');assert abs(plan['rows'][0]['exitStart']-plan['rows'][0]['entryEnd']-4.5)<.001
  page.evaluate("state.speed=1;document.getElementById('speed').value=1;zeParagraphModel.cache=null")
  # Controlled Arabic text is captured into its own transparent test canvas.
  # Verify movement reverses with Flip and no text pixels escape the fixed panel mask.
  page.locator('#bullets').fill('نص تجريبي واضح\n\nفقرة أخرى جديدة');page.evaluate('zeParagraphModel.items.forEach(r=>r.manual=2);zeParagraphModel.cache=null;zeSetVideoDuration(12)')
  plan=page.evaluate('zeParagraphSchedule()');first=plan['rows'][0];second=plan['rows'][1]
  for flipped in [False,True]:
   page.evaluate('(v)=>setFlipped(v)',flipped)
   points=[]
   for time in [first['exitStart'],first['exitStart']+first['exit']*.2]:
    png=page.evaluate('''(time)=>{const canvas=document.createElement('canvas');canvas.width=960;canvas.height=540;const ctx=canvas.getContext('2d');ctx.textBaseline='middle';zeDrawParagraphText(ctx,time,{x:100,y:150,w:400,h:200,wrap:350,textWidth:350,right:470,baseline:35,lineHeight:35,font:24});return canvas.toDataURL()}''',time)
    im=np.array(Image.open(io.BytesIO(base64.b64decode(png.split(',')[1]))));ys,xs=np.where(im[:,:,3]>0);assert len(xs)>0,(flipped,time,page.evaluate("zeParagraphPhase("+str(time)+")"));assert xs.min()>=101 and xs.max()<499 and ys.min()>=151 and ys.max()<349;points.append(xs.mean())
   assert points[1]>points[0] if flipped else points[1]<points[0],points
   phases=page.evaluate('(t)=>zeParagraphPhases(t)',second['start']+.1);assert {first['id'],second['id']}=={phase['row']['id'] for phase in phases}
  # Compare actual composed frames with/without text in both source paths and flips.
  for imported in [False,True]:
   if imported:
    page.locator('#postFiles').set_input_files(str(root/'tests/fixtures/photo.png'));page.wait_for_function('zePost.active')
   for protected in [False,True]:
    page.evaluate('(v)=>document.getElementById("protectLowerThird").checked=v',protected)
    for flipped in [False,True]:
     page.evaluate('(v)=>setFlipped(v)',flipped);plan=page.evaluate('zeParagraphSchedule()')
     for time in [plan['rows'][0]['exitStart']+.1,plan['rows'][1]['start']+.25]:
      check=page.evaluate("""(t)=>{setT(t);const panel=zeVisibleBounds('bullet',getBBox('bullet')),a=c.getImageData(0,0,1920,1080).data,good=zeDrawParagraphText;zeDrawParagraphText=()=>{};draw();const b=c.getImageData(0,0,1920,1080).data;zeDrawParagraphText=good;draw();let changed=0,outside=0;for(let i=0;i<a.length;i+=4){if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3]){changed++;const x=(i/4)%1920/2,y=Math.floor(i/4/1920)/2;if(x<panel.x-1||x>panel.x+panel.w+1||y<panel.y-1||y>panel.y+panel.h+1)outside++}}return {changed,outside}}""",time)
      assert check['outside']==0,(imported,protected,flipped,time,check)
  page.evaluate('document.getElementById("protectLowerThird").checked=true;setFlipped(false)')
  # Transparent pixels are real alpha in the exported image, with clean redraws after background-on.
  page.locator('#transparentOutput').check();page.evaluate('setT(4)');alpha=page.evaluate('c.getImageData(0,0,1,1).data[3]');assert alpha==0
  assert page.locator('#recordFull').is_disabled() and page.locator('#record').is_disabled();assert 'final render engine' in page.locator('#exportProgress').inner_text()
  with page.expect_download() as image:page.locator('#still').click()
  image.value.save_as('/tmp/ze-beta26-alpha.png');im=np.array(Image.open('/tmp/ze-beta26-alpha.png'));assert im.shape[2]==4 and im[:,:,3].min()==0 and im[:,:,3].max()==255
  page.locator('#transparentOutput').uncheck();assert page.evaluate('c.getImageData(0,0,1,1).data[3]')==255
  # Timing and final MOV-alpha intent survive the existing project JSON export.
  page.locator('#transparentOutput').check()
  with page.expect_download() as scene:page.locator('#saveJson').click()
  scene.value.save_as('/tmp/ze-beta26-scene.json');data=json.loads(Path('/tmp/ze-beta26-scene.json').read_text());assert data['output']['background']=='transparent' and '4444' in data['output']['requestedFinalCodec'];assert data['videoTiming']['durationSeconds']==12
  page.locator('#transparentOutput').uncheck();page.locator('#showBullets').uncheck();page.locator('#videoDuration').fill('5.2');page.locator('#videoDuration').press('Tab')
  with page.expect_download(timeout=20000) as video:page.locator('#recordFull').click()
  video.value.save_as('/tmp/ze-beta26-full-5.2.webm');duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','/tmp/ze-beta26-full-5.2.webm']));assert abs(duration-5.2)<.35,duration
  page.locator('#recordFull').click();page.wait_for_function('state.recording');page.locator('#cancelRecord').click();page.wait_for_function('!state.recording');assert not page.locator('#videoDuration').is_disabled()
  page.locator('#videoDuration').fill('8');page.locator('#videoDuration').press('Tab');page.evaluate('setT(8)');page.locator('#play').click();page.wait_for_timeout(150);assert page.evaluate('state.t<1')
  assert not page.evaluate('state.renderError');assert not errors,errors
  print('Auto/manual paragraph holds, edits/reorder/duplicates, duration overflow, reverse masked exits, alpha PNG, JSON, full video duration and cancel: passed')
  browser.close()
finally:server.shutdown();server.server_close()

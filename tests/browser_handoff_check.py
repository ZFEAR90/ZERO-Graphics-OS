"""Staggered line handoff, collision clipping, persistent final text and solo-roll language."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading,json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1920,'height':1080});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('state.stvLoaded && assets.source');page.evaluate("document.getElementById('bulletSplitMode').value='blank'");page.locator('#respectSafeArea').click()
  page.locator('#portraitLayout').select_option('focus',force=True)  # Explicit legacy adaptive treatment; reference default has its own check.
  cases=[['نص قصير جديد','هذه فقرة طويلة لاختبار تتابع الأسطر وعدم تداخل الكلمات داخل اللوحة السوداء. '*6],['هذه فقرة طويلة لاختبار سرعة خروج كل سطر مع دخول الفقرة التالية. '*7,'نص آخر'],['A short line','A longer English paragraph with mixed Arabic كلمات عربية to verify a safe line handoff. '*5],['فقرة أولى للاختبار '*18,'فقرة ثانية '*15,'النص الأخير يبقى على الشاشة']]
  for case in cases:
   page.locator('#bullets').fill('\n\n'.join(case));page.evaluate('zeParagraphModel.items.forEach(row=>row.manual=.8);zeParagraphModel.cache=null;zeSetVideoDuration(50)')
   for flipped in [False,True]:
    page.evaluate('(v)=>setFlipped(v)',flipped)
    result=page.evaluate('''(()=>{
     const plan=zeParagraphSchedule(),b=zeBulletTextBox(),canvas=document.createElement('canvas');canvas.width=960;canvas.height=540;const ctx=canvas.getContext('2d');ctx.textBaseline='middle';let frames=0,twoVisible=0,staggered=false;
     for(let n=0;n<plan.rows.length-1;n++){
      const row=plan.rows[n],next=plan.rows[n+1];if(!(next.start<row.end))throw Error('No paragraph overlap');
      for(let t=row.exitStart+.02;t<Math.max(row.end,next.entryEnd);t+=.04){
       const lines=zeParagraphRenderLines(ctx,t,b),visible=lines.map(line=>({...line,l:Math.max(line.left,line.clipLeft,b.x+1),r:Math.min(line.right,line.clipRight,b.x+b.w-1),a:Math.max(line.top,b.y+1),z:Math.min(line.bottom,b.y+b.h-1)})).filter(line=>line.r>line.l&&line.z>line.a&&line.alpha>.001);
       if(new Set(visible.map(line=>line.rowId)).size>1)twoVisible++;
       const exits=visible.filter(line=>line.rowId===row.id);if(exits.length>1&&exits.some(line=>line.exit>0&&line.exit<1)&&exits.some(line=>line.exit===0))staggered=true;
       for(let i=0;i<visible.length;i++)for(let j=i+1;j<visible.length;j++){const a=visible[i],c=visible[j];if(a.r>c.l+.001&&c.r>a.l+.001&&a.z>c.a+.001&&c.z>a.a+.001)throw Error('Glyph bounds collide: '+JSON.stringify([a,c]))}
       ctx.clearRect(0,0,960,540);zeDrawParagraphText(ctx,t,b);const pixels=ctx.getImageData(0,0,960,540).data;let count=0;for(let i=3;i<pixels.length;i+=4)if(pixels[i]>0)count++;if(!count)throw Error('Empty panel at '+t);frames++;
      }
     }
     const final=plan.rows.at(-1);if(final.exit!==0||final.exitStart!==null)throw Error('Final paragraph exits');
     for(const t of [Math.max(final.entryEnd,final.holdEnd)+.2,49.98,50])if(t<=50){if(!zeParagraphRenderLines(ctx,t,b).some(line=>line.rowId===final.id&&line.alpha>.9))throw Error('Final text missing')}
     return {frames,twoVisible,staggered,rows:plan.rows.map(row=>({lines:row.lineCount,start:row.start,end:row.end,exitStart:row.exitStart}))};
    })()''')
    assert result['twoVisible']>0,result
    if any(r['lines']>1 for r in result['rows'][:-1]):assert result['staggered'],result
    print('Handoff',flipped,result['frames'],'frames,',result['twoVisible'],'overlap frames',flush=True)
  # One final paragraph is readable at the exact video end even with a short manual hold.
  page.locator('#bullets').fill('هذا النص الأخير يبقى على الشاشة');page.evaluate('zeParagraphModel.items[0].manual=1;zeParagraphModel.cache=null;setT(50)');assert page.evaluate('zeParagraphPhase(50).row.final')
  # Larger solo roll and safe central header, with correct source direction for both scripts.
  page.evaluate('setT(5);setFlipped(false)');with_bullets=page.evaluate('getBBox("source")');page.locator('#showBullets').uncheck();solo=page.evaluate('getBBox("source")');assert solo['w']>with_bullets['w'] and abs(solo['x']+solo['w']/2-480)<.01
  def check_safe():
   data=page.evaluate('({area:zeBroadcastBounds(),source:getBBox("source"),header:zeHeaderPaintBounds(getBBox("identity")),focus:zeCenteredPortrait()})');a=data['area'];s=data['source'];h=data['header'];assert s['x']>=a['x'] and s['x']+s['w']<=a['x']+a['w'];assert s['y']>=a['y'] and s['y']+s['h']<=(508 if data['focus'] else a['bottom'])+.01;assert h['y']>=34 and h['x']>=a['x']+102 and h['x']+h['w']<=a['x']+a['w']-102;assert h['y']+h['h']<s['y']
  check_safe()
  page.locator('#allowMediaOverlap').check();page.locator('#postFiles').set_input_files(str(root/'tests/fixtures/portrait.mp4'));page.wait_for_function('zePost.active');page.locator('#postContentMode').select_option('media');portrait=page.evaluate('getBBox("source")');assert portrait['w']>200 and portrait['h']>350;check_safe()
  page.locator('#rollLanguage').select_option('rtl');assert page.evaluate('zeHeaderFlipped()')
  page.locator('#rollLanguage').select_option('ltr');assert not page.evaluate('zeHeaderFlipped()');page.locator('#rollLanguage').select_option('auto')
  page.locator('#postContentMode').select_option('text');page.locator('#postBody').fill('هذه فقرة عربية مع بعض الأرقام 123');assert page.evaluate('zeRollDirection()')=='rtl';page.locator('#postBody').fill('An English article with numbers 123');assert page.evaluate('zeRollDirection()')=='ltr';check_safe()
  page.locator('#rollLanguage').select_option('rtl');assert page.evaluate('zeRollDirection()')=='rtl'
  # One diagonal gesture uses the destination X position to release the top-corner limit.
  page.locator('#showBullets').check();page.locator('#sourceFile').set_input_files(str(root/'tests/fixtures/landscape.mp4'));page.wait_for_function('zePost.items.length===1 && zePost.items[0].label==="landscape.mp4"');page.locator('#postContentMode').select_option('media');page.evaluate("state.screenOffsets={identity:{x:0,y:0},source:{x:0,y:0},bullet:{x:0,y:0}};document.getElementById('compositionX').value=0;document.getElementById('compositionY').value=0;setFlipped(false)")
  page.evaluate("state.screenOffsets.bullet={x:0,y:-300};draw()");side=page.evaluate('({bullet:getBBox("bullet"),header:zeHeaderPaintBounds(getBBox("identity"))})');assert side['header']['y']>=76
  page.evaluate("state.screenOffsets.bullet={x:170,y:-300};draw()");middle=page.evaluate('({bullet:getBBox("bullet"),header:zeHeaderPaintBounds(getBBox("identity"))})');assert abs(middle['header']['y']-34)<.01;assert middle['bullet']['y']<side['bullet']['y']-30,(side,middle)
  page.evaluate("state.screenOffsets.bullet={x:0,y:-300};draw()");assert page.evaluate('zeHeaderPaintBounds(getBBox("identity")).y')>=76
  print('Moving diagonally into the clear middle releases the corner limit; returning to a side restores it',flush=True)
  assert not page.evaluate('state.renderError');assert not errors,errors;print('Final hold and enlarged, safe, language-aware solo roll: passed',flush=True);browser.close()
finally:server.shutdown();server.server_close()

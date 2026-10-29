"""Owner's final adjustments: real controls, retained geometry, masks and strict text safety."""
from pathlib import Path
from http.server import ThreadingHTTPServer
import importlib.util,threading,json,os
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('helper',root/'ze_local_importer.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
class Handler(helper.Handler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
out=Path(os.environ.get('ZE_FINAL_EVIDENCE_DIR','/tmp/ze-browser-evidence/final-adjustments'));out.mkdir(parents=True,exist_ok=True)
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1600,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('assets.source&&state.stvLoaded')
  def tab(id):return page.locator('#'+id).evaluate("el=>el.closest('.editor-tab-panel')?.id")
  for id in ['postUrl','useMainRoll','useWholePost','bullets','showBullets','postFiles','postTextPlacement','postMediaFit','account','displayname','respectSafeArea','mainDuration','accentColor','panelColor','textColor','saveJson']:
   assert tab(id)=='mainOptions',(id,tab(id))
  for id in ['compositionX','compositionY','allowMediaOverlap','layerScale','fontSize','justifyMode','kashidaStrength','postJustifyMode','socialTextSize','mediaPresentation','mediaTransitionDuration','paletteStrength','frameColor','safeAreas','paragraphTimings']:
   assert tab(id)=='advancedOptions',(id,tab(id))
  assert page.locator('.sidebar.right').count()==0 and page.locator('#renderVideo').is_visible()
  assert not page.locator('#advancedMediaPanel').evaluate('el=>el.open')
  page.locator('#postFiles').set_input_files(str(root/'tests/fixtures/landscape.mp4'));page.wait_for_function('zePost.items.length===1&&zePost.items[0].el.readyState>=2&&!zePost.items[0].el.seeking')
  assert page.locator('#postMediaList input').count()==1
  assert page.get_by_role('checkbox',name='Protect face region for landscape.mp4',include_hidden=True).evaluate("el=>el.closest('.editor-tab-panel').id")=='advancedOptions'
  page.locator('#openMediaDetails').click();assert page.locator('#advancedTab').get_attribute('aria-selected')=='true' and page.locator('#advancedMediaPanel').evaluate('el=>el.open')
  page.locator('#advancedPostMediaList details').evaluate('(el)=>el.open=true')
  field=page.get_by_role('spinbutton',name='Face left for landscape.mp4');field.fill('20');field.press('Tab');assert page.evaluate('zePost.items[0].framing.protectFace&&zePost.items[0].framing.face.x===20')
  page.locator('#mainTab').click();page.locator('#useWholePost').click();assert not page.locator('#showBullets').is_checked()
  page.locator('#openMediaDetails').click();pin=page.get_by_role('checkbox',name='Keep landscape.mp4 visible while post scrolls');assert not pin.is_checked();pin.check();assert page.locator('#postScrollMode').input_value()=='fixed'
  page.locator('#mainTab').click();page.locator('#useWholePost').click();assert page.locator('#postScrollMode').input_value()=='fixed' # Active presentation preserves overrides.
  page.locator('#openMediaDetails').click();pin.uncheck();assert page.locator('#postScrollMode').input_value()=='together'
  page.locator('#mainTab').click()
  print('Main essentials, Advanced geometry/framing/colors, regenerated media controls, speaker toggle and active-layout overrides: passed',flush=True)
  # Hidden text uses the same sharp, centered media renderer even in retained Advanced layouts.
  for layout in ['reference','social','focus','balanced','beside']:
   for flip in [False,True]:
    paint=page.evaluate("""v=>{document.getElementById('portraitLayout').value=v.layout;zeSocialControls(true);document.getElementById('postTextPlacement').value='hidden';document.getElementById('postContentMode').value='all';setFlipped(v.flip);const out=document.createElement('canvas');out.width=600;out.height=300;const ctx=out.getContext('2d'),filters=[],filter=Object.getOwnPropertyDescriptor(CanvasRenderingContext2D.prototype,'filter');Object.defineProperty(ctx,'filter',{get(){return filter.get.call(ctx)},set(value){filters.push(value);filter.set.call(ctx,value)}});zeDrawPost(ctx,0,0,600,300,5);const a=ctx.getImageData(0,0,600,300).data;return {filters,painted:Array.from(a).some((v,i)=>i%4===3&&v>0)}}""",dict(layout=layout,flip=flip))
    assert paint['painted'] and not any('blur' in f for f in paint['filters']),(layout,flip,paint)
  print('Hidden/media-only post renders without duplicate blur in primary and retained Advanced layouts, both flips: passed',flush=True)
  page.evaluate("document.getElementById('postTextPlacement').value='roll'")
  # Geometry changes only when explicitly moved, never as a Text-only side effect.
  matrix=[]
  text='هذه فقرة عربية طويلة للاختبار؛ يجب أن يبقى النص آمناً فوق الخبر العاجل. '*70
  page.locator('#postBody').fill(text)
  for layout in ['reference','social']:
   page.evaluate('(v)=>{document.getElementById("portraitLayout").value=v;zeSocialControls(true)}',layout)
   for flip in [False,True]:
    for bullets in [False,True]:
     for protect in [False,True]:
      result=page.evaluate('''v=>{document.getElementById('showBullets').checked=v.bullets;document.getElementById('protectLowerThird').checked=v.protect;document.getElementById('allowMediaOverlap').checked=!v.protect;setFlipped(v.flip);document.getElementById('postContentMode').value='all';zeInvalidatePost();const before=structuredClone(zeSafeLayout()),media=zePost.layoutMedia.slice();document.getElementById('postContentMode').value='text';zeInvalidatePost();const text=structuredClone(zeSafeLayout());document.getElementById('postContentMode').value='all';zeInvalidatePost();return {before,text,after:zeSafeLayout(),sameMedia:media.length===zePost.layoutMedia.length&&media.every((i,n)=>i===zePost.layoutMedia[n])}}''',dict(flip=flip,bullets=bullets,protect=protect))
      assert result['before']==result['text']==result['after'] and result['sameMedia'],(layout,flip,bullets,protect,result)
      matrix.append(dict(layout=layout,flip=flip,bullets=bullets,protect=protect))
  print('Text only preserves source/header/bullet rectangles and original media geometry across 16 normal/flipped combinations: passed',flush=True)
  # Normal guide mode has a lower boundary than the stricter breaking-news line.
  # Prove actual text pixels respect the latter even when roll protection is off.
  safety=[]
  for layout in ['reference','social']:
   page.evaluate('(v)=>{document.getElementById("portraitLayout").value=v;zeSocialControls(true)}',layout)
   for flip in [False,True]:
    result=page.evaluate('''v=>{document.getElementById('showBullets').checked=false;document.getElementById('postContentMode').value='text';document.getElementById('protectLowerThird').checked=false;document.getElementById('lowerThirdMode').value='normal';document.getElementById('breakingNewsTop').value=740;document.getElementById('lowerThirdTop').value=900;setFlipped(v);zeUpdateSafePreview();const old=zeDrawSocialText;let changed=0,outside=0;for(const t of [2.2,5,25,49.96]){setT(t);const a=c.getImageData(0,0,1920,1080).data;zeDrawSocialText=()=>{};draw();const b=c.getImageData(0,0,1920,1080).data;zeDrawSocialText=old;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3]){changed++;if(Math.floor(i/4/1920)>=zeTextSafeBottom()*2)outside++}}draw();return {changed,outside,bottom:zeTextSafeBottom()}}''',flip)
    assert result['changed']>50 and result['outside']==0,(layout,flip,result);safety.append(dict(layout=layout,flip=flip,**result))
    page.evaluate('setT(5)');page.locator('#canvas').screenshot(path=str(out/f'{layout}-text-only-{int(flip)}.png'))
  print('Painted text-only pixels remain above the breaking-news boundary in Main/Whole, normal/flipped, with protection off: passed',flush=True)
  # Visually inspect representative settled normal/flipped full scenes and their header gap.
  page.evaluate("document.getElementById('breakingNewsTop').value=847;document.getElementById('lowerThirdMode').value='breaking';document.getElementById('portraitLayout').value='reference';zeSocialControls(true);document.getElementById('postContentMode').value='all';document.getElementById('postTextPlacement').value='roll';document.getElementById('bullets').value='نص مستقل يبقى مرئياً';document.getElementById('showBullets').checked=true;document.getElementById('protectLowerThird').checked=true;document.getElementById('allowMediaOverlap').checked=false;zeUpdateSafePreview();draw()")
  headers=[]
  for flip in [False,True]:
   page.evaluate('(v)=>setFlipped(v)',flip);page.evaluate('setT(5)')
   h=page.evaluate("(()=>{const h=zeHeaderPaintBounds(getBBox('identity')),b=zeVisibleBounds('bullet',getBBox('bullet'));return {h,b,source:getBBox('source'),bottom:zeTextSafeBottom(),gap:b.y-h.y-h.h}})()");assert abs(h['gap']-24)<.01 and h['source']['y']+h['source']['h']<=h['bottom'],h;headers.append(h)
   page.screenshot(path=str(out/f'workspace-{int(flip)}.png'));page.locator('#canvas').screenshot(path=str(out/f'main-{int(flip)}.png'))
  assert not errors and not page.evaluate('state.renderError'),errors
  (out/'validation.json').write_text(json.dumps({'geometry_combinations':matrix,'painted_text_safety':safety,'painted_headers':headers,'browser_errors':errors},indent=2)+'\n')
  print('Normal/flipped header screenshots, 24-unit painted gap, and zero JavaScript errors: passed',flush=True);browser.close()
finally:server.shutdown();server.server_close()

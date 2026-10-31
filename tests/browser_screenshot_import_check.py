"""Actual offline Arabic/English reader, editable review/crops, and normal post import."""
from browser_support import scene,ROOT
from pathlib import Path
with scene('screenshot-import') as s:
 p=s.page;browser=p.context.browser
 fixture=browser.new_page();fixture.set_viewport_size({'width':900,'height':1100});fixture.set_content('''<html><body style="margin:0;background:white;font:26px Arial;color:#18212e"><div style="padding:20px;background:#0866ff;color:white">facebook</div><div style="position:absolute;left:40px;top:105px;width:70px;height:70px;border-radius:50%;background:#108fd0;color:white;text-align:center;line-height:70px">A</div><b style="position:absolute;left:135px;top:110px">Example Author</b><span style="position:absolute;left:135px;top:148px">@example</span><div style="position:absolute;top:205px;left:40px">Original screenshot post text for this test.<br>مرحبا هذا نص عربي داخل المنشور</div><div style="position:absolute;left:60px;top:340px;width:760px;height:600px;background:linear-gradient(#087eaf,#90d5e8);border-bottom:60px solid #d91f31"><div style="font:bold 45px Arial;color:white;text-align:center;padding-top:180px">POST PHOTO</div></div></body></html>''');target=Path('/tmp/ze-screenshot-source.png');fixture.screenshot(path=str(target));fixture.close()
 external=[];p.context.on('request',lambda r:external.append(r.url) if r.url.startswith(('http://','https://')) and not r.url.startswith(s.url+'/') else None)
 s.value('bullets','Keep this independent editorial bulletin')
 p.locator('#postScreenshotFile').set_input_files(str(target));p.wait_for_function("document.getElementById('screenshotStatus').textContent.startsWith('Screenshot read.') || document.getElementById('screenshotStatus').textContent.includes('manually.')",timeout=120000)
 status=p.locator('#screenshotStatus').inner_text();assert status.startswith('Screenshot read.'),status
 assert p.locator('#screenshotPlatform').input_value()=='Facebook',p.evaluate('zeScreenshotAnalysis.getReadText()')
 extracted=p.locator('#screenshotText').input_value();assert 'Original screenshot' in extracted,extracted
 assert any('\u0600'<=c<='\u06ff' for c in extracted),extracted
 assert p.locator('#screenshotHasMedia').is_checked()
 # Real user review corrects uncertain fields and image boundaries without replacing the whole scene.
 s.value('screenshotName','Reviewed author');s.value('screenshotHandle','@reviewed');s.value('screenshotText','Original screenshot post text.\nمرحبا هذا نص عربي');s.value('screenshotCropTarget','media')
 for k,value in dict(x=60/9,y=340/11,w=760/9,h=660/11).items():s.value('screenshotCrop'+k,str(value))
 s.value('screenshotCropTarget','profile')
 for k,value in dict(x=40/9,y=105/11,w=70/9,h=70/11).items():s.value('screenshotCrop'+k,str(value))
 s.value('screenshotHasProfile',True);s.value('screenshotHasMedia',True);p.locator('#applyScreenshot').click();p.wait_for_function("zePost.active && document.getElementById('displayname').value==='Reviewed author'")
 assert p.evaluate("zeSolo.postPlatform==='Facebook'&&zePost.items.length===1&&assets.avatar!==null&&zePostRollText().includes('مرحبا')")
 assert p.locator('#bullets').input_value()=='Keep this independent editorial bulletin'
 assert p.locator('#showRollAccount').is_checked() and p.locator('#showPostText').is_checked()
 assert not external,external
 for t in [.8,1.2,2.12,5]:
  p.evaluate('(t)=>setT(t)',t);p.locator('#canvas').screenshot(path=f'/tmp/ze-main-post-entrance-{t}.png')
 p.locator('#canvas').screenshot(path='/tmp/ze-screenshot-imported.png')
 p.locator('#useWholePost').click();p.locator('#wholeFrameArrangement').select_option('below');p.locator('#postMediaFit').select_option('fill');p.evaluate('setT(20)');p.locator('#canvas').screenshot(path='/tmp/ze-whole-post-fill.png')
 print('Actual bundled Arabic/English screenshot reader ran without external requests; review, profile/media crops and normal editable post import preserve bulletin: passed')

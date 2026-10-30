"""Owner's October 30 examples: defaults, sentence/point pagination, pinned title and palette."""
from browser_support import scene, ROOT
with scene('owner-adjustments') as s:
 p=s.page;s.post('هذه مقدمة خبرية كاملة.\n\nهذه فقرة ثانية كاملة.',('landscape.mp4',));s.all_controls()
 assert p.locator('#linkImport').get_attribute('open') is not None
 assert p.locator('#postTextPlacement').input_value()=='bullet'
 assert p.locator('#postScrollMode').input_value()=='together'
 assert p.locator('#postMediaFit').input_value()=='fit'
 assert p.evaluate("zePostRollText()===''&&zeSocialRegions(100,100,400,300).text===null")
 assert p.locator('#bullets').input_value()==p.locator('#postBody').input_value()
 assert p.evaluate('''()=>{const im=document.createElement('canvas');im.width=800;im.height=200;const x=im.getContext('2d');x.fillStyle='green';x.fillRect(0,0,800,200);x.fillStyle='red';x.fillRect(0,0,100,200);x.fillStyle='blue';x.fillRect(700,0,100,200);const out=document.createElement('canvas');out.width=280;out.height=360;const ctx=out.getContext('2d');zeDrawCleanMedia(ctx,im,0,0,280,360,zePost.items[0],true);const left=ctx.getImageData(5,180,1,1).data,right=ctx.getImageData(275,180,1,1).data;return left[0]===255&&right[2]===255&&ctx.getImageData(140,5,1,1).data[3]===0}''')
 # Complete sentences should move to the next page instead of splitting at the capacity line.
 result=p.evaluate('''()=>{const b={font:18,wrap:260,baseline:20,lineHeight:30,h:120,w:280};const sentences=['This sentence describes the first event in full.','This sentence describes the second event in full.','This sentence describes the third event in full.'];const pages=zePaginateBullet(sentences.join(' '),b);return {pages,sentences,fits:pages.every(v=>zeBulletLineCount(v,b)<=zeBulletLineCapacity(b))}}''')
 assert result['fits'] and len(result['pages'])>1,result
 assert p.evaluate(r'''()=>{const pages=zePaginateBullet('1. This is the first sentence of a long numbered point. This is another complete sentence. This is the final complete sentence.',{font:18,wrap:220,baseline:20,lineHeight:30,h:120,w:240});return pages.length>1&&pages.every(p=>p.trim()!=='1.'&&!/\n1\.$/.test(p))}''')
 assert all(any(sentence in page for page in result['pages']) for sentence in result['sentences']),result
 title='قراءة في نتائج الانتخابات والأسباب التالية:'
 points=[f'{i}. هذا سبب مستقل يشرح النتيجة السياسية والاقتصادية بصورة كاملة وواضحة.' for i in range(1,9)]
 source=title+'\n\n'+'\n\n'.join(points);s.value('bullets',source)
 assert p.evaluate('zeBulletTitleInfo().title')==title
 assert p.evaluate('zeBulletTextBox().y>zeBaseBulletTextBox().y+20')
 pages=p.evaluate('zeBulletPageValues(document.getElementById("bullets").value)')
 assert len(pages)>1 and all(title not in page for page in pages)
 assert all(any(point in page for page in pages) for point in points),pages
 assert p.evaluate('zeParagraphSchedule().rows.every(r=>r.lineCount<=zeBulletLineCapacity(zeBulletTextBox()))')
 s.value('bulletPinnedTitle','عنوان مخصص');assert p.evaluate('zeBulletTitleInfo().title')=='عنوان مخصص'
 saved=p.evaluate('zeProjectData()');s.value('bulletPinnedTitle','');p.evaluate('async data=>zeApplyProject(data)',saved);assert p.evaluate('zeBulletTitleInfo().title')=='عنوان مخصص'
 s.value('bulletPinnedTitle','')
 # Stationary title pixels while the body switches pages, in normal and flipped layouts.
 for flip in [False,True]:
  s.value('flip',flip)
  pixels=p.evaluate('''()=>{const b=zeBulletTitleBox(),snap=t=>{setT(t);return [...c.getImageData(Math.ceil((b.x+4)*2),Math.ceil((b.y+4)*2),Math.floor((b.w-8)*2),Math.floor((b.h-8)*2)).data]};return [snap(5),snap(30)]}''')
  assert pixels[0]==pixels[1]
  assert p.evaluate('zeBulletTextBox().y+zeBulletTextBox().h<=zeTextSafeBottom()')
 p.locator('#normalBullet').click();assert p.evaluate('zeBulletTitleInfo()===null')
 assert p.locator('#bullets').input_value()==source
 # Main's manual text-in-roll option must share motion, with Whole also defaulting to it.
 s.value('postTextPlacement','roll');assert p.evaluate('zeScrollTogether()')
 p.locator('#useWholePost').click();assert p.evaluate('zeScrollTogether()&&!document.getElementById("showBullets").checked')
 # Actual background imports drive the panel color; manual choice is persistent and reversible.
 p.locator('#backgroundFile').set_input_files(str(ROOT/'tests/fixtures/photo.png'));p.wait_for_function('zeSolo.palette!==null');old=p.locator('#panelColor').input_value()
 p.locator('#backgroundFile').set_input_files(str(ROOT/'tests/fixtures/portrait.png'));p.wait_for_function('(old)=>document.getElementById("panelColor").value!==old',arg=old)
 s.value('panelColor','#194555');assert p.locator('#lockPanelColor').is_checked()
 p.evaluate("zeSetPalette('#aa5533')");assert p.evaluate("zeElementColor('bulletPanel')")== '#194555'
 s.value('lockPanelColor',False);assert p.locator('#panelColor').input_value()!='#194555'
 assert p.evaluate("(()=>{const c=document.createElement('canvas');c.width=96;c.height=54;const x=c.getContext('2d');x.fillStyle='#777777';x.fillRect(0,0,96,54);return zeAnalyzeColors(c)==='#777777'})()")
 print('Main media-only/Fit import, shared-scroll override, semantic boundaries, pinned title pixels/reset, and automatic/manual panel palette: passed')

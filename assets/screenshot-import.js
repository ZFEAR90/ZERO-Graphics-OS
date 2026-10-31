/* Local screenshot recognition and editable crop review. No screenshot leaves this browser. */
(() => {
 const panel=document.createElement('section');panel.id='screenshotImport';panel.innerHTML=`
 <label class="label" for="postScreenshotFile">Import post screenshot</label>
 <input id="postScreenshotFile" type="file" accept="image/*"/>
 <p class="micro" id="screenshotStatus" role="status">If the link fails, choose a screenshot. Read and review its platform, account, text and media before importing. Screenshots cannot recover video or audio.</p>
 <details id="screenshotReview" hidden><summary>Review screenshot post</summary>
 <button id="readScreenshot" type="button">Read screenshot</button>
 <label class="label" for="screenshotPlatform">Platform</label><select id="screenshotPlatform"><option value="">Choose platform</option>${['X','Facebook','Instagram','Telegram','Threads'].map(x=>`<option>${x}</option>`).join('')}</select>
 <label class="label" for="screenshotName">Account name</label><input id="screenshotName"/>
 <label class="label" for="screenshotHandle">Account handle</label><input id="screenshotHandle"/>
 <label class="label" for="screenshotText">Post text · correct any reading errors</label><textarea id="screenshotText" rows="6"></textarea>
 <label class="check"><input id="screenshotHasProfile" type="checkbox"/>Use cropped profile picture</label>
 <label class="check"><input id="screenshotHasMedia" type="checkbox"/>Post contains an image</label>
 <label class="label" for="screenshotCropTarget">Select a crop to adjust</label><select id="screenshotCropTarget"><option value="media">Post image · blue outline</option><option value="profile">Profile picture · orange outline</option></select>
 <p class="micro">Drag over the screenshot to select the profile or post image. Include text painted into an image in that image crop. Keep the account row outside the post-image crop.</p>
 <div style="max-height:420px;overflow:auto"><canvas id="screenshotCanvas" style="display:block;max-width:100%;height:auto;touch-action:none;cursor:crosshair"></canvas></div>
 <div class="scalegrid" id="screenshotCropFields">${['x','y','w','h'].map(k=>`<label>${({x:'Left',y:'Top',w:'Width',h:'Height'})[k]} %<input id="screenshotCrop${k}" type="number" min="0" max="100" step=".1"/></label>`).join('')}</div>
 <button id="applyScreenshot" type="button" class="primary">Import reviewed screenshot post</button>
 </details>`;
 $('importPost').parentElement.after(panel);
 const status=$('screenshotStatus'),review=$('screenshotReview'),preview=$('screenshotCanvas');
 const model={image:null,profile:{x:2,y:3,w:12,h:12},media:{x:0,y:30,w:100,h:70},worker:null,sequence:0};
 const clampPct=n=>Math.max(0,Math.min(100,Number(n)||0));
 function rect(value){const x=clampPct(value.x),y=clampPct(value.y);return {x,y,w:Math.max(.1,Math.min(100-x,clampPct(value.w))),h:Math.max(.1,Math.min(100-y,clampPct(value.h)))}}
 function paint(){if(!model.image)return;const ratio=Math.min(1,640/model.image.width);preview.width=Math.round(model.image.width*ratio);preview.height=Math.round(model.image.height*ratio);const ctx=preview.getContext('2d');ctx.drawImage(model.image,0,0,preview.width,preview.height);for(const [key,color] of [['media','#0787ff'],['profile','#f28b19']]){if(!$(key==='media'?'screenshotHasMedia':'screenshotHasProfile').checked)continue;const r=model[key];ctx.strokeStyle=color;ctx.lineWidth=3;ctx.strokeRect(r.x*preview.width/100,r.y*preview.height/100,r.w*preview.width/100,r.h*preview.height/100)}}
 function fields(){const r=model[$('screenshotCropTarget').value];for(const k of ['x','y','w','h'])$('screenshotCrop'+k).value=r[k].toFixed(1);paint()}
 $('screenshotCropTarget').onchange=fields;
 for(const k of ['x','y','w','h'])$('screenshotCrop'+k).oninput=()=>{const key=$('screenshotCropTarget').value;model[key]=rect(Object.fromEntries(['x','y','w','h'].map(n=>[n,$('screenshotCrop'+n).value])));$(key==='media'?'screenshotHasMedia':'screenshotHasProfile').checked=true;paint()};
 for(const id of ['screenshotHasMedia','screenshotHasProfile'])$(id).onchange=paint;
 let start=null;
 const point=e=>{const b=preview.getBoundingClientRect();return {x:clampPct((e.clientX-b.left)/b.width*100),y:clampPct((e.clientY-b.top)/b.height*100)}};
 preview.onpointerdown=e=>{start=point(e);preview.setPointerCapture(e.pointerId)};
 preview.onpointermove=e=>{if(!start)return;const end=point(e),key=$('screenshotCropTarget').value;model[key]=rect({x:Math.min(start.x,end.x),y:Math.min(start.y,end.y),w:Math.abs(end.x-start.x),h:Math.abs(end.y-start.y)});$(key==='media'?'screenshotHasMedia':'screenshotHasProfile').checked=true;fields()};
 preview.onpointerup=preview.onpointercancel=()=>{start=null};
 function crop(r){const im=model.image,canvas=document.createElement('canvas'),x=Math.round(im.width*r.x/100),y=Math.round(im.height*r.y/100);canvas.width=Math.max(1,Math.round(im.width*r.w/100));canvas.height=Math.max(1,Math.round(im.height*r.h/100));canvas.getContext('2d').drawImage(im,x,y,canvas.width,canvas.height,0,0,canvas.width,canvas.height);return canvas.toDataURL('image/png')}
 function guessPlatform(text){for(const [platform,re] of [['Telegram',/telegram|t\.me\//i],['Facebook',/facebook|fb\.com|فيسبوك/i],['Instagram',/instagram|انستغرام/i],['Threads',/threads\.com|threads\.net|\bthreads\b/i],['X',/twitter|x\.com\/|تويتر/i]])if(re.test(text))return platform;return ''}
 function linesOf(data){const lines=[];for(const block of data.blocks||[])for(const paragraph of block.paragraphs||[])for(const line of paragraph.lines||[])if(line.text?.trim())lines.push({text:line.text.trim(),bbox:line.bbox,confidence:line.confidence});return lines}
 // Image regions are proposals. The review canvas always allows correcting or excluding them.
 function mediaProposal(canvas,lines,headerBottom){const maxW=400,scale=Math.min(1,maxW/canvas.width),w=Math.round(canvas.width*scale),h=Math.round(canvas.height*scale),small=document.createElement('canvas');small.width=w;small.height=h;const ctx=small.getContext('2d');ctx.drawImage(canvas,0,0,w,h);const pixels=ctx.getImageData(0,0,w,h).data,mask=new Uint8Array(w*h);
  for(const line of lines){const b=line.bbox;for(let y=Math.max(0,Math.floor(b.y0*scale)-2);y<Math.min(h,Math.ceil(b.y1*scale)+2);y++)for(let x=Math.max(0,Math.floor(b.x0*scale)-2);x<Math.min(w,Math.ceil(b.x1*scale)+2);x++)mask[y*w+x]=1}
  const rows=[];for(let y=Math.ceil(headerBottom*scale);y<h;y++){let count=0,left=w,right=0;for(let x=0;x<w;x++){const i=(y*w+x)*4,r=pixels[i],g=pixels[i+1],b=pixels[i+2],colored=Math.max(r,g,b)-Math.min(r,g,b)>28,detailed=x>0&&Math.abs(r-pixels[i-4])>25;if(!mask[y*w+x]&&(colored||detailed)&&Math.min(r,g,b)<235){count++;left=Math.min(left,x);right=Math.max(right,x)}}if(count>w*.09)rows.push({y,left,right})}
  let best=[],group=[];for(const row of rows){if(group.length&&row.y-group.at(-1).y>Math.max(9,h*.025)){if(group.length>best.length)best=group;group=[]}group.push(row)}if(group.length>best.length)best=group;
  if(!best.length||best.at(-1).y-best[0].y<h*.09)return null;const left=Math.max(0,Math.min(...best.map(r=>r.left))-4),right=Math.min(w,Math.max(...best.map(r=>r.right))+4),top=Math.max(0,best[0].y-4),bottom=Math.min(h,best.at(-1).y+4);return rect({x:left/w*100,y:top/h*100,w:(right-left)/w*100,h:(bottom-top)/h*100})}
 async function worker(){if(model.worker)return model.worker;if(location.protocol==='file:')throw Error('Open the connected editor using START_ZE_OS.bat to read the screenshot automatically. You can still enter the text and select image crops here.');
  if(!window.Tesseract)await new Promise((resolve,reject)=>{const script=document.createElement('script');script.src='assets/screenshot-reader/tesseract.min.js';script.onload=resolve;script.onerror=()=>reject(Error('Screenshot reader files are missing. Extract the entire ZIP.'));document.head.append(script)});
  const base=new URL('assets/screenshot-reader/',location.href).href;
  model.worker=await Tesseract.createWorker(['eng','ara'],1,{workerPath:base+'worker.min.js',corePath:base,langPath:base,gzip:true,workerBlobURL:false,cacheMethod:'none',logger:m=>{if(m.status==='recognizing text')status.textContent='Reading screenshot… '+Math.round(m.progress*100)+'%'}});return model.worker;
 }
 async function readPlatformHeader(reader){
  const canvas=document.createElement('canvas');canvas.width=model.image.width;canvas.height=Math.max(40,Math.round(model.image.height*.17));const ctx=canvas.getContext('2d');ctx.drawImage(model.image,0,0);const data=ctx.getImageData(0,0,canvas.width,canvas.height),a=data.data;
  for(let y=0;y<canvas.height;y++){let color=0;for(let x=0;x<canvas.width;x++){const i=(y*canvas.width+x)*4;if(Math.max(a[i],a[i+1],a[i+2])-Math.min(a[i],a[i+1],a[i+2])>30)color++}if(color>canvas.width*.3)for(let x=0;x<canvas.width;x++){const i=(y*canvas.width+x)*4,v=(a[i]+a[i+1]+a[i+2])/3>185?0:255;a[i]=a[i+1]=a[i+2]=v}}
  ctx.putImageData(data,0,0);await reader.setParameters({tessedit_pageseg_mode:'6'});try{return guessPlatform((await reader.recognize(canvas,{}, {text:true})).data.text||'')}finally{await reader.setParameters({tessedit_pageseg_mode:'3'})}
 }
 async function read(){if(!model.image)return;const sequence=model.sequence;$('readScreenshot').disabled=true;status.textContent='Reading screenshot locally. Review the result before importing.';
  try{const reader=await worker(),result=await reader.recognize(model.image,{}, {text:true,blocks:true});if(sequence!==model.sequence)return;const data=result.data;model.recognizedText=data.text;const lines=linesOf(data),height=model.image.height,width=model.image.width,hint=guessPlatform(data.text||'')||zeRecognizePlatform($('postUrl').value).platform||await readPlatformHeader(reader);if(sequence!==model.sequence)return;$('screenshotPlatform').value=hint;
   const upper=lines.filter(l=>l.bbox.y0<height*.28&&!/^(telegram|facebook|instagram|threads|for you|following|search|back)$/i.test(l.text)),handle=upper.find(l=>/@[\w.]+/.test(l.text));let name=handle?upper[upper.indexOf(handle)-1]:upper[0];if(!name)name=upper[0];
   $('screenshotName').value=name?.text||'';$('screenshotHandle').value=handle?.text.match(/@[\w.]+/)?.[0]||'';
   const headerBottom=Math.max(name?.bbox.y1||0,handle?.bbox.y1||0)+height*.018;
   if(name){const size=Math.min(width*.16,Math.max(30,(name.bbox.y1-name.bbox.y0)*2.5));model.profile=rect({x:Math.max(0,name.bbox.x0-size-10)/width*100,y:Math.max(0,name.bbox.y0-4)/height*100,w:size/width*100,h:size/height*100})}
   // An initial-only profile is also a usable crop; keep this explicitly reviewable.
   $('screenshotHasProfile').checked=!!name&&name.bbox.x0>width*.07;
   const media=mediaProposal(model.image,lines,headerBottom);if(media)model.media=media;$('screenshotHasMedia').checked=!!media;
   const inMedia=line=>{if(!media)return false;const b=line.bbox,cx=(b.x0+b.x1)/2/width*100,cy=(b.y0+b.y1)/2/height*100;return cx>=media.x&&cx<=media.x+media.w&&cy>=media.y&&cy<=media.y+media.h};
   const body=lines.filter(l=>l!==name&&l!==handle&&l.bbox.y0>=headerBottom-height*.01&&!inMedia(l)&&!/^\s*(like|comment|share|reply|repost|views|send|إعجاب|مشاركة|تعليق)\b/i.test(l.text));$('screenshotText').value=body.length?body.map(l=>l.text).join('\n'):(lines.length?'':data.text||'');fields();
   status.textContent='Screenshot read. Check platform, account, text and crop outlines, then import. Photo regions are suggestions; correct them with a drag.';
  }catch(error){status.textContent=(error?.message||String(error))+' Use the review fields to complete the post manually.'}finally{if(sequence===model.sequence)$('readScreenshot').disabled=false}
 }
 $('postScreenshotFile').onchange=async e=>{const file=e.target.files[0];if(!file)return;if(file.size>20*1024*1024){status.textContent='Choose an image smaller than 20 MiB.';return}const url=URL.createObjectURL(file);try{const image=await zeReadPostImage(url);if(image.width*image.height>32000000)throw Error('Screenshot is too large. Crop it to the post first.');const factor=Math.min(1,1600/image.width,10000/image.height),canvas=document.createElement('canvas');canvas.width=Math.round(image.width*factor);canvas.height=Math.round(image.height*factor);canvas.getContext('2d').drawImage(image,0,0,canvas.width,canvas.height);model.image=canvas;model.sequence++;review.hidden=false;review.open=true;$('screenshotPlatform').value='';$('screenshotName').value='';$('screenshotHandle').value='';$('screenshotText').value='';$('screenshotHasProfile').checked=false;$('screenshotHasMedia').checked=false;model.media={x:0,y:30,w:100,h:70};fields();await read()}catch(error){status.textContent=error.message}finally{URL.revokeObjectURL(url);e.target.value=''}};
 $('readScreenshot').onclick=read;
 $('applyScreenshot').onclick=async()=>{const platform=$('screenshotPlatform').value;if(!platform){status.textContent='Choose the platform before importing the screenshot.';return}if(!model.image)return;const button=$('applyScreenshot');button.disabled=true;try{const text=$('screenshotText').value,name=$('screenshotName').value.trim(),handle=$('screenshotHandle').value.trim(),attachments=$('screenshotHasMedia').checked?[{type:'image',data_url:crop(model.media)}]:[],prepared=await zePreparePost({text,name,handle,attachments}),avatar=$('screenshotHasProfile').checked?await zeReadPostImage(crop(model.profile)):null;
  zeApplyDetection({platform,url:$('postUrl').value,account:handle.replace(/^@/,'')});$('displayname').value=name;$('account').value=handle;assets.avatar=avatar;zeCommitPost(prepared);assets.source=zePostDocument();assets.sourceBottom=null;draw();status.textContent='Screenshot imported as an editable post. External bulletin kept. Verify against the screenshot; original video/audio cannot be recovered.';zeSetStatus('Reviewed screenshot post loaded.',true);
 }catch(error){status.textContent='Screenshot was not imported: '+error.message+' Existing scene was kept.'}finally{button.disabled=false}};
 // Expose only pure analysis for deterministic fixture checks.
 window.zeScreenshotAnalysis={guessPlatform,linesOf,mediaProposal,getReadText:()=>model.recognizedText};
})();

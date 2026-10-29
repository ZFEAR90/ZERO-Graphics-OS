"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('post-justification') as s:
 p=s.page;text=('هذا نص عربي آمن يحافظ على اتصال الحروف وترتيب الكلمات داخل المنشور. '*20).strip()+'\nالسطر الأخير'
 s.post(text);p.locator('#useWholePost').click();assert p.locator('#postJustifyMode').input_value()=='kashida'
 result=p.evaluate("""()=>{const doc=zeSocialTextDocument(240);let justified=0,natural=0;for(const line of doc.lines){c.font=line.style;const a=justifyLine(c,line.text,440,line.final?'none':'kashida',1);if(line.final){if(a.words.join(' ')!==line.text)throw Error('Final line changed');natural++}else{if(Math.abs(a.total-440)>1)throw Error('Line not justified');if(a.words.some(w=>w.includes('ـ')))justified++}if(a.words.map(w=>w.replace(/ـ/g,'')).join(' ')!==line.text)throw Error('Glyph or word order changed')}return {justified,natural,safe:['اا','دب','لا','رى'].every(w=>stretchWord(c,w,200)===w)}}""")
 assert result['justified']>0 and result['natural']>=2 and result['safe'],result
 assert p.locator('#postBody').input_value()==text
 print('Joining-safe kashida fills non-final lines; natural final lines, word/glyph order and stored source remain unchanged: passed')

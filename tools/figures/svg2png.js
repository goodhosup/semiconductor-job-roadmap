const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:900,height:400},deviceScaleFactor:2});
const [dir,out]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.svg'))){await p.goto('file://'+path.resolve(dir,f));const el=await p.$('svg');await el.screenshot({path:path.join(out,f.replace('.svg','.png')),omitBackground:true});}
await b.close();})();

import asyncio, base64, re, pathlib
from playwright.async_api import async_playwright
B=pathlib.Path('/tmp/ig')  # fuentes descargadas con: npm pack @fontsource/schibsted-grotesk @fontsource/hanken-grotesk (descomprimir aquí)
SVG=pathlib.Path(__file__).parent/'simbolo.svg'
def f64(p): return base64.b64encode(p.read_bytes()).decode()
S=B/'fontsource-schibsted-grotesk-5.3.0/files'; H=B/'fontsource-hanken-grotesk-5.3.0/files'
fonts="".join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{f64(d/f'{fn}-latin-{w}-normal.woff2')})}}" for n,d,fn,ws in [('S',S,'schibsted-grotesk',[700,800]),('H',H,'hanken-grotesk',[400,500,600])] for w in ws)
svg=SVG.read_text()
logo=svg; water=svg.replace('#2D2D2D','#EEEAE5')
def uri(s): return 'data:image/svg+xml;base64,'+base64.b64encode(s.encode()).decode()
CSS=f"""{fonts}*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1350px;background:#fff;font-family:H;color:#2D2D2D;position:relative;overflow:hidden}}
.w{{position:absolute;right:-330px;top:260px;width:1000px;opacity:1}}.top{{position:absolute;left:90px;top:90px;display:flex;align-items:center;gap:22px;font-size:38px;color:#4F4B47;font-weight:500}}.top img{{width:72px}}
.c{{position:absolute;left:90px;right:90px;top:300px}}h1{{font-family:S;font-weight:800;font-size:104px;line-height:1.02;letter-spacing:-2px}}h1.m{{font-size:84px}}
.bar{{width:150px;height:12px;background:#D08A3A;margin:56px 0}}p{{font-size:42px;line-height:1.35;color:#4F4B47;max-width:860px}}p b{{color:#2D2D2D;font-weight:600}}
.k{{font-family:S;font-weight:800;color:#9A581C}}.foot{{position:absolute;left:90px;bottom:90px;right:90px;display:flex;justify-content:space-between;font-size:32px;color:#68645F}}
ol{{list-style:none;padding:0;margin-top:20px}}li{{font-size:44px;line-height:1.3;margin:0 0 34px;padding-left:80px;position:relative;color:#2D2D2D}}li span{{position:absolute;left:0;top:-4px;font-family:S;font-weight:800;color:#D08A3A;font-size:52px}}
.pill{{display:inline-block;background:#2D2D2D;color:#fff;font-family:S;font-weight:700;font-size:44px;padding:28px 44px;border-radius:999px;margin-top:20px}}"""
def page(body,foot=""):
    return f"<html><head><style>{CSS}</style></head><body><img class=w src='{uri(water)}'><div class=top><img src='{uri(logo)}'>amonita.cl</div><div class=c>{body}</div><div class=foot>{foot}</div></body></html>"
import json,sys
semana=pathlib.Path(sys.argv[1]); OUT=semana
spec=json.loads((semana/'posts.json').read_text())
P={k:page(v['html'],v.get('foot','')) for k,v in spec.items()}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1080,'height':1350})
        for k,h in P.items():
            await pg.set_content(h); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT/f'{k}.jpg'),type='jpeg',quality=92)
        await b.close()
asyncio.run(main())

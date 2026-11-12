"""Genera un Reel vertical (1080x1920, 30 fps, H.264) a partir de 2026/semana-NN/reel.json.
reel.json: {"nombre": "reel", "escenas": [{"html": "...", "foot": "...", "dur": 4}, ...]}
Uso: python3 herramientas/reel.py 2026/semana-NN   (requiere las fuentes en /tmp/ig, ver README)"""
import asyncio, json, sys, pathlib, subprocess, os
here = pathlib.Path(__file__).parent
src = (here/'render.py').read_text()
ns = {'__file__': str(here/'render.py')}
exec(src[:src.index('import json,sys')], ns)          # reutiliza fuentes, marca y page()
ns['CSS'] = ns['CSS'].replace('height:1350px', 'height:1920px').replace('top:300px', 'top:560px').replace('top:260px', 'top:620px').replace('top:90px', 'top:250px').replace('bottom:90px', 'bottom:430px')
page = lambda h, f: ns['page'].__code__ and eval('page(h,f)', ns, {'h': h, 'f': f})
semana = pathlib.Path(sys.argv[1]); spec = json.loads((semana/'reel.json').read_text())
tmp = pathlib.Path('/tmp/reel_build'); tmp.mkdir(exist_ok=True)
from playwright.async_api import async_playwright
async def shots():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for i, e in enumerate(spec['escenas']):
            await pg.set_content(page(e['html'], e.get('foot', ''))); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(tmp/f'e{i}.jpg'), type='jpeg', quality=92)
        await b.close()
asyncio.run(shots())
lista = []
for i, e in enumerate(spec['escenas']):
    d = float(e.get('dur', 4)); out = tmp/f'e{i}.part.mp4'
    vf = (f"scale=1080:1920,format=yuv420p,loop=-1:1,trim=duration={d},"
          f"zoompan=z='1+0.0004*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
          f"fade=in:st=0:d=0.35,fade=out:st={d-0.35}:d=0.35,setpts=PTS-STARTPTS")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', str(tmp/f'e{i}.jpg'), '-vf', vf,
                    '-r', '30', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', str(out)], check=True)
    os.replace(out, tmp/f'e{i}.mp4'); lista.append(f"file '{tmp/f'e{i}.mp4'}'")
(tmp/'lista.txt').write_text('\n'.join(lista))
final = semana/f"{spec.get('nombre','reel')}.mp4"
# Instagram exige pista de audio en algunos casos: se agrega silencio
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(tmp/'lista.txt'),
                '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
                '-movflags', '+faststart', str(final)], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '1', '-i', str(final), '-frames:v', '1', '-q:v', '3', str(semana/f"{spec.get('nombre','reel')}_portada.jpg")], check=True)
print(final)

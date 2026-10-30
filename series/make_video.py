"""Offline cloud render. Voice is pre-generated; no API credentials are needed."""
from pathlib import Path
import os,sys,json,subprocess,time,re
P=Path(__file__).resolve().parent;name=sys.argv[1];cfg=json.loads((P/'profiles'/name/'timing.json').read_text());out=P/'out'/name;out.mkdir(parents=True,exist_ok=True)
if (out/'picture.mp4').exists():raise SystemExit('Output exists; use a fresh output directory')
st=time.monotonic();env=os.environ|{'POLYMATH_PROFILE':name,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'};frames=round(cfg['duration']*30)
subprocess.run([sys.executable,str(P/'render.py'),'0',str(frames),str(out/'picture.mp4')],env=env,check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(out/'picture.mp4'),'-i',str(P/'vo'/name/'voice.flac'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(cfg['duration']),'-movflags','+faststart',str(out/'voice-preview.mp4')],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out/'voice-preview.mp4')]))
v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',frames)
assert a['sample_rate']=='48000' and a['channels']==2
r=subprocess.run(['ffmpeg','-hide_banner','-xerror','-i',str(out/'voice-preview.mp4'),'-vf','freezedetect=n=0.002:d=2','-f','null','-'],capture_output=True,text=True,check=True);(out/'decode.log').write_text(r.stderr)
starts=[float(x) for x in re.findall(r'freeze_start: ([\d.]+)',r.stderr)];ends=[float(x) for x in re.findall(r'freeze_end: ([\d.]+)',r.stderr)];events=[]
for i,s in enumerate(starts):
 e=ends[i] if i<len(ends) else cfg['duration'];allowed=any(s>=lo-.25 and e<=hi+.25 for lo,hi in cfg.get('intentional_holds',[]));events.append({'start':s,'end':e,'intentional':allowed})
assert all(x['intentional'] for x in events),events
points=[round(i*(frames-10)/29) for i in range(30)];expr='+'.join('eq(n,'+str(i)+')' for i in points);vf="select='"+expr+"',scale=180:320,tile=10x3"
subprocess.run(['ffmpeg','-v','error','-i',str(out/'voice-preview.mp4'),'-vf',vf,'-frames:v','1','-q:v','2',str(out/'contact.jpg')],check=True)
r={'name':name,'status':'passed','duration':cfg['duration'],'frames':frames,'dimensions':[1080,1920],'fps':30,'shots':len(cfg['shots']),'render_seconds':round(time.monotonic()-st,2),'freeze_events':events,'scope':'Technical image/voice preview validation; final music mix is performed locally. Human listening, mobile review and viewer retention are not inferred.'}
(out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False))

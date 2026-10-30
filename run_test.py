from pathlib import Path
import subprocess,time,json,sys
P=Path(__file__).resolve().parent;P.joinpath('out').mkdir(exist_ok=True);P.joinpath('qa').mkdir(exist_ok=True)
st=time.monotonic()
subprocess.run([sys.executable,str(P/'render.py'),'0','180',str(P/'out/picture.mp4')],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(P/'out/picture.mp4'),'-i',str(P/'vo/test.flac'),'-map','0:v','-map','1:a','-c:v','copy','-af','loudnorm=I=-16:TP=-2:LRA=11','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t','6','-movflags','+faststart',str(P/'out/test-polymath.mp4')],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(P/'out/test-polymath.mp4')]))
v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert [v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames'])]==[1080,1920,'30/1',180]
assert a['sample_rate']=='48000' and a['channels']==2
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(P/'out/test-polymath.mp4'),'-f','null','-'],check=True)
r={'status':'passed','render_seconds':round(time.monotonic()-st,2),'frames':180,'duration':float(probe['format']['duration']),'dimensions':[1080,1920],'audio':'AAC 48kHz stereo','scope':'Technical six-second render; not an editorial or retention validation.'};(P/'qa/result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))

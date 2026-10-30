"""Le Polymath: native 1080p animated engravings; cached raster art and fast PIL compositing."""
from pathlib import Path
import json,math,sys,subprocess,bisect
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageEnhance,ImageFilter
P=Path(__file__).resolve().parent;W,H,FPS=1080,1920,30
CFG=json.loads((P/'timing.json').read_text());DUR=CFG['duration'];S=CFG['shots'];STARTS=[s[0] for s in S]
G=(232,184,74);WHITE=(245,240,230);RED=(155,25,31)
def font(f,n,weight):
 x=ImageFont.truetype(str(P/'fonts'/f'{f}.ttf'),n);x.set_variation_by_name(weight);return x
FS=font('Montserrat',58,'ExtraBold');FH=font('Playfair',65,'Black');FL=font('Montserrat',46,'ExtraBold');FB=font('Montserrat',31,'Bold');FC=font('Montserrat',23,'Bold');FN=font('Playfair',245,'Black')
WORDS=json.loads((P/'words_tl.json').read_text());GROUPS=[];cur=[]
for w in WORDS:
 test=cur+[w];width=sum(FS.getlength(z['disp'].upper()) for z in test)+16*(len(test)-1)
 if cur and (len(cur)>=3 or width>800):GROUPS.append(cur);cur=[]
 cur.append(w)
 if w['disp'].rstrip().endswith(('.',',','?',':','!')):GROUPS.append(cur);cur=[]
if cur:GROUPS.append(cur)
GS=[g[0]['start'] for g in GROUPS]
AS={}
def asset(name):
 if name not in AS:
  im=Image.open(P/'assets'/f'{name}.webp').convert('RGBA');im.thumbnail((760,850));AS[name]=im
 return AS[name]
tex=Image.open(P/'img/black_marble.jpg').convert('RGB').resize((W,H),Image.Resampling.BILINEAR)
BGS={}
for name,c,blend in [('black',(8,8,9),.68),('red',(112,13,24),.86),('gold',(159,112,35),.86),('white',(229,222,205),.94)]:BGS[name]=Image.blend(tex,Image.new('RGB',(W,H),c),blend).convert('RGBA')
# Vignette prepared once; all lettering and artwork are composited at native resolution.
y,x=np.mgrid[0:480,0:270];rad=np.sqrt(((x-135)/180)**2+((y-210)/310)**2);v=np.uint8(np.clip(rad*.68,0,.76)*255);vig=Image.new('RGBA',(270,480),(0,0,0,0));vig.putalpha(Image.fromarray(v));vig=vig.resize((W,H),Image.Resampling.BILINEAR)
for n in BGS:BGS[n].alpha_composite(vig)
def ease(u):return 1-(1-min(1,max(0,u)))**3
def paste(c,im,cx=540,cy=800,scale=1,rot=0):
 if abs(scale-1)>.002:im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.BILINEAR)
 if rot:im=im.rotate(rot,resample=Image.Resampling.BILINEAR,expand=True)
 c.alpha_composite(im,(round(cx-im.width/2),round(cy-im.height/2)))
def text(c,txt,y,f=FL,col=WHITE,x=540,stroke=2):
 ImageDraw.Draw(c).text((x,y),txt,font=f,fill=col,anchor='mm',stroke_width=stroke,stroke_fill=(8,7,6))
def fittext(c,txt,y,size=64,maxw=850,col=G):
 f=font('Playfair',size,'Black')
 if f.getlength(txt)>maxw:f=font('Playfair',int(size*maxw/f.getlength(txt)),'Black')
 text(c,txt,y,f,col)
def rays(c,t):
 overlay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(overlay);cx,cy=540,810
 for i in range(22):
  a=i*2*math.pi/22+t*.065; b=a+.07
  d.polygon([(cx,cy),(cx+1700*math.cos(a),cy+1700*math.sin(a)),(cx+1700*math.cos(b),cy+1700*math.sin(b))],fill=G+(25,))
 c.alpha_composite(overlay)
def frieze(c,y):
 d=ImageDraw.Draw(c);d.line((225,y,855,y),fill=G,width=4)
 for x in range(230,850,35):d.line([(x,y+15),(x,y+5),(x+24,y+5),(x+24,y+25),(x+9,y+25),(x+9,y+15),(x+16,y+15)],fill=G,width=3)
def crown(c,x,y,u,scale=1):
 d=ImageDraw.Draw(c);pts=[(x-85*scale,y),(x-85*scale,y-70*scale),(x-35*scale,y-30*scale),(x,y-90*scale),(x+35*scale,y-30*scale),(x+85*scale,y-70*scale),(x+85*scale,y),(x-85*scale,y)]
 k=min(len(pts),max(2,int(u*len(pts))));d.line(pts[:k],fill=G,width=7)
BILLS={}
def bill(value):
 if value not in BILLS:
  im=Image.new('RGBA',(780,400));d=ImageDraw.Draw(im);d.rounded_rectangle((14,14,766,386),20,fill=(227,216,187),outline=G,width=7);d.rectangle((35,35,745,365),outline=(65,49,29),width=3)
  for k in range(55,350,12):d.line((50,k,170,k-20),fill=(135,110,66),width=1);d.line((610,k-20,730,k),fill=(135,110,66),width=1)
  d.ellipse((230,55,550,345),outline=(120,90,40),width=4);d.text((390,195),f'{value} $',font=font('Playfair',155,'Black'),fill=(30,25,18),anchor='mm');d.text((390,337),'EXPÉRIENCE',font=FC,fill=(70,55,34),anchor='mm');BILLS[value]=im
 return BILLS[value]
def stamp(c,label,u):
 if u<0:return
 im=Image.new('RGBA',(820,150));d=ImageDraw.Draw(im);d.rounded_rectangle((7,7,813,143),12,outline=(223,40,40),width=10);f=font('Montserrat',min(76,int(740/max(1,len(label))/.65)),'ExtraBold');d.text((410,75),label,font=f,fill=(223,40,40),anchor='mm')
 paste(c,im,540,1170,1+.3*math.exp(-u*20),-8)
def subs(c,t):
 j=max(0,bisect.bisect_right(GS,t+.02)-1);g=GROUPS[j];widths=[FS.getlength(w['disp'].upper()) for w in g];x=540-(sum(widths)+16*(len(g)-1))/2;d=ImageDraw.Draw(c)
 for w,wd in zip(g,widths):
  if t>=w['start']-.02:
   txt=w['disp'].upper();dy=8*(1-ease((t-w['start']+.02)/.12));d.text((x,1395+dy),txt,font=FS,fill=G if w['key'] else WHITE,anchor='lm',stroke_width=3,stroke_fill=(5,5,5))
   if w['key']:d.line((x,1440,x+wd*ease((t-w['start'])/.12),1440),fill=G,width=5)
  x+=wd+16

def frame(t):
 i=max(0,bisect.bisect_right(STARTS,t)-1);st,kind,p=S[i];end=STARTS[i+1] if i+1<len(S) else DUR;lt=t-st;progress=lt/max(.1,end-st);c=BGS[p.get('bg','black')].copy();entry=ease(lt/.18);pop=1+.10*math.sin(min(1,lt/.32)*math.pi)*math.exp(-lt*2)
 if p.get('rays') or kind in ['duel','brain','choice']:rays(c,t)
 dx=(1-entry)*p.get('direction',1)*240 if i else 0
 scale=(.8+.2*entry)*pop*(1+.045*progress);floaty=10*math.sin(t*2.5)
 if kind=='duel':
  paste(c,bill(1),290-dx,820+25*math.sin(lt*3),.53*pop,-8+3*math.sin(lt*4));paste(c,bill(20),790+dx,860-25*math.sin(lt*3),.53*pop,8-3*math.sin(lt*4));text(c,'VS',670,FH,G)
  if lt>.55:crown(c,290,665-.0*lt,ease((lt-.55)/.2),.65)
  fittext(c,'LE PLUS CONVAINCANT ?',1120,56)
 elif kind=='money':
  value=p.get('value',1)
  if value==20:
   for n in [2,1]:paste(c,bill(value),540+n*20,825+n*20,.9*scale,(-1)**n*4)
  paste(c,bill(value),540+dx,800+floaty,.95*scale,4*math.sin(lt*5))
  if value==1 and lt>.5:crown(c,540,565,ease((lt-.5)/.2))
  fittext(c,p.get('label','UNE JUSTIFICATION'),1150,62)
 elif kind=='pegs':
  board=Image.new('RGBA',(830,650));d=ImageDraw.Draw(board);d.rounded_rectangle((5,5,825,645),22,fill=(180,157,112),outline=G,width=8)
  for row in range(6):
   for col in range(8):
    n=row*8+col;a=math.pi*.5*ease((lt*9-n%8)*1.4);cx=72+col*98;cy=72+row*99;pts=[(cx+27*math.cos(a+math.pi/4+k*math.pi/2),cy+27*math.sin(a+math.pi/4+k*math.pi/2)) for k in range(4)];d.polygon(pts,fill=(35,30,23),outline=(243,230,192))
  paste(c,board,540+dx,810,scale,-5+3*math.sin(lt));text(c,'ENCORE. ENCORE. ENCORE.',1210,FC,G)
  d=ImageDraw.Draw(c);cx,cy=850,450;d.ellipse((cx-65,cy-65,cx+65,cy+65),outline=G,width=6);a=lt*10;d.line((cx,cy,cx+48*math.sin(a),cy-48*math.cos(a)),fill=WHITE,width=5)
 elif kind in ['subject','brain','mask']:
  name=p.get('img',{'brain':'brain','mask':'mask'}.get(kind,'student'))
  if kind=='mask':
   paste(c,asset('student'),540,840,.78*scale)
   paste(c,asset('mask'),540+dx,650-20*math.cos(lt*3),.65*scale,-10*(1-entry))
  else:
   bounce=-28*math.sin(min(1,max(0,lt-.5)/.25)*math.pi) if kind=='brain' else floaty
   paste(c,asset(name),540+dx,800+bounce,p.get('scale',.95)*scale,3*math.sin(lt*3)*p.get('wobble',1))
  if p.get('label'):fittext(c,p['label'],360,68)
  if kind=='brain':stamp(c,p.get('stamp','PAS SI NUL !'),lt-.65)
  if p.get('stamp') and kind!='brain':stamp(c,p['stamp'],lt-.5)
  if p.get('extra') and lt>.35:text(c,p['extra'],570,FN,G,x=840)
 elif kind=='year':
  s=1+.65*math.exp(-lt*12);im=Image.new('RGBA',(1000,440));ImageDraw.Draw(im).text((500,220),'1959',font=FN,fill=(25,20,14),anchor='mm');paste(c,im,540,820,s)
  frieze(c,580);frieze(c,1040);text(c,'FESTINGER & CARLSMITH',1140,font('Montserrat',40,'ExtraBold'),G)
 elif kind=='conflict':
  d=ImageDraw.Draw(c)
  for side,label,col in [(-1,"C'ÉTAIT NUL",(105,18,25)),(1,"J'AI DIT : GÉNIAL",(96,72,26))]:
   x=540+side*(215+230*(1-entry));d.rounded_rectangle((x-210,650,x+210,990),22,fill=col,outline=G,width=5)
   words=label.split();text(c,' '.join(words[:2]),770,font('Montserrat',38,'ExtraBold'),WHITE,x=x);text(c,' '.join(words[2:]),850,font('Montserrat',38,'ExtraBold'),G,x=x)
  text(c,'≠',1110,FN,G)
 elif kind=='concept':
  txt='DISSONANCE';k=min(len(txt),int(lt/.035)+1);fittext(c,txt[:k],770,116);fittext(c,'COGNITIVE',930,100);frieze(c,620);frieze(c,1040)
  if lt>.65:text(c,'QUAND ÇA SE CONTREDIT',1170,font('Montserrat',36,'ExtraBold'),WHITE)
 elif kind=='choice':
  paste(c,asset('philo_cut'),540+dx,760,.85*scale)
  text(c,'UNE RAISON',1110,FL,G);text(c,'OU UNE JUSTIFICATION ?',1190,font('Montserrat',39,'ExtraBold'),WHITE)
 elif kind=='result':
  paste(c,bill(1),285,740,.5*scale,-4);paste(c,bill(20),795,740,.5*scale,4)
  text(c,'PLUS',1010,FL,G,x=285);text(c,'INTÉRESSANTE',1080,font('Montserrat',31,'ExtraBold'),G,x=285)
  text(c,'MOINS',1010,FL,WHITE,x=795);text(c,'INTÉRESSANTE',1080,font('Montserrat',31,'ExtraBold'),WHITE,x=795)
  if lt>.4:crown(c,285,560,ease((lt-.4)/.18),.8)
 # Short transition accents; typography is drawn afterwards for legibility.
 tr=p.get('tr','whip')
 if i and lt<.12:
  u=1-lt/.12
  if tr=='whip':c=c.filter(ImageFilter.BoxBlur(3*u));shift=round(55*u*p.get('direction',1));tmp=BGS[p.get('bg','black')].copy();tmp.alpha_composite(c,(shift,0));c=tmp
  elif tr=='impact':
   over=Image.new('RGBA',(W,H),(245,233,205,round(70*u)));c.alpha_composite(over)
  elif tr=='red':c.alpha_composite(Image.new('RGBA',(W,H),(180,22,28,round(60*u))))
 if t<3:
  text(c,'UNE EXPÉRIENCE ÉTONNANTE',185,FC,WHITE)
  fittext(c,'1 $ CONVAINC MIEUX',280,64);fittext(c,'QUE 20 $',365,64)
 subs(c,t);text(c,'LE POLYMATH',1515,FB,G,stroke=1);text(c,'Festinger & Carlsmith · 1959',1570,FC,WHITE,stroke=1)
 return np.asarray(c.convert('RGB'))
if __name__=='__main__':
 if sys.argv[1]=='still':Image.fromarray(frame(float(sys.argv[2]))).save(sys.argv[3]);raise SystemExit()
 a,b,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
 proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-preset','veryfast','-threads','2','-crf','16','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
 for n in range(a,b):proc.stdin.write(frame(n/30).tobytes())
 proc.stdin.close();rc=proc.wait()
 if rc:raise SystemExit(rc)

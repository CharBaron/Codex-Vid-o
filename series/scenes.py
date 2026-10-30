"""Domain-specific visual demonstrations; geometry stays in the TikTok safe area."""
import math
from PIL import Image,ImageDraw

def draw(c,kind,p,t,lt,progress,scale,dx,a):
 text,fit,paste,asset,font,crown=[a[x] for x in ['text','fittext','paste','asset','font','crown']];G=a['G'];WHITE=a['WHITE'];FL=a['FL'];FH=a['FH'];FN=a['FN'];FC=a['FC'];ease=a['ease'];d=ImageDraw.Draw(c)
 if kind=='calendar':
  d.rounded_rectangle((240,510,840,1100),25,fill=(232,221,191),outline=G,width=8)
  day=p.get('day','2');day=str(day)
  if p.get('jump'):day='2' if lt<.5 else '14'
  text(c,'SEPTEMBRE 1752',580,font('Montserrat',35,'ExtraBold'),(45,34,20))
  text(c,day,815,font('Playfair',235,'Black'),(28,23,18))
  for i in range(11):
   age=lt-.35-i*.045
   if p.get('jump') and age>0:
    im=Image.new('RGBA',(100,130),(228,214,180,240));ImageDraw.Draw(im).text((50,65),str(i+3),font=font('Playfair',43,'Black'),fill=(25,22,18),anchor='mm');paste(c,im,540+420*math.sin(i*1.3)*min(1,age*2),730-400*min(1,age*1.3),.8,age*100)
  fit(c,p.get('label','ONZE DATES SAUTÉES'),1190,58)
 elif kind=='orbit':
  d.ellipse((290,550,790,1050),outline=G,width=5);d.ellipse((465,725,615,875),fill=(232,177,66),outline=WHITE,width=4)
  angle=t*1.2;x=540+250*math.cos(angle);y=800+250*math.sin(angle);d.ellipse((x-26,y-26,x+26,y+26),fill=(190,204,189),outline=G,width=4);fit(c,'LE CALENDRIER SUIT LE SOLEIL',1180,51)
 elif kind=='ship':
  phase=p.get('phase','replace')
  if phase=='replace':
   paste(c,asset('ship'),540+dx,770,.98*scale,3*math.sin(lt*3));n=int(progress*12)
   for i in range(12):d.rounded_rectangle((232+i*52,1030,274+i*52,1095),4,fill=G if i<n else (220,211,183),outline=(55,43,25),width=2)
   fit(c,'LES PIÈCES CHANGENT',1190,58)
  else:
   paste(c,asset('ship'),300-dx/2,790,.46*scale,-3);paste(c,asset('ship'),740+dx/2,790,.46*scale,3)
   text(c,'A',550,FH,G,x=300);text(c,'B',550,FH,G,x=740)
   text(c,'CONTINUITÉ',1060,font('Montserrat',40,'ExtraBold'),G,x=300);text(c,"MATIÈRE",1060,font('Montserrat',40,'ExtraBold'),WHITE,x=740)
   for i in range(5):
    u=(lt*.7+i*.17)%1;x=320+440*u;y=930-120*math.sin(math.pi*u);d.rounded_rectangle((x-26,y-9,x+26,y+9),3,fill=(185,145,75),outline=G,width=2)
   if phase=='duel':fit(c,'QUI GARDE LE NOM ?',1200,60)
 elif kind=='blindspot':
  # Both marks remain genuinely present and fixed. No artificial disappearance.
  d.ellipse((190,830,230,870),fill=WHITE);d.line((835,830,875,870),fill=WHITE,width=8);d.line((835,870,875,830),fill=WHITE,width=8)
  text(c,'ŒIL GAUCHE FERMÉ',510,font('Montserrat',44,'ExtraBold'),G)
  text(c,'FIXE LE POINT À GAUCHE',590,font('Montserrat',42,'ExtraBold'),WHITE)
  text(c,"APPROCHE DOUCEMENT L'ÉCRAN",1210,font('Montserrat',34,'ExtraBold'),G)
  text(c,'La distance dépend de ton écran.',1395,font('Montserrat',29,'Bold'),WHITE)
 elif kind=='retina':
  d.ellipse((240,500,840,1100),outline=WHITE,width=8);d.arc((265,525,815,1075),-115,115,fill=G,width=13)
  for i in range(22):
   ang=-1.8+i*3.6/21;x=540+270*math.cos(ang);y=800+270*math.sin(ang)
   if abs(ang)>.13:d.ellipse((x-7,y-7,x+7,y+7),fill=G)
  d.line((810,800,950,850),fill=G,width=22);d.line((750,1110,815,825),fill=WHITE,width=4);fit(c,'SORTIE DU NERF OPTIQUE',1190,53)
 elif kind=='offers':
  paste(c,asset('chocolate'),540+dx,710,.85*scale,4*math.sin(lt*3))
  free=p.get('free',False);left='GRATUIT' if free else '1 ¢';right='14 ¢' if free else '15 ¢'
  for x,label in [(285,left),(795,right)]:
   d.rounded_rectangle((x-205,980,x+205,1110),15,fill=(30,25,20),outline=G,width=5);text(c,label,1045,font('Playfair',65,'Black'),G,x=x)
  text(c,'CENTS DE DOLLAR',1200,FC,WHITE)
  if free and lt>.4:crown(c,285,960,ease((lt-.4)/.2),.7)
 elif kind=='zero':
  text(c,'0',810,font('Playfair',400,'Black'),G);fit(c,'UN PRIX À PART',1170,65)
  if lt>.35:crown(c,540,565,ease((lt-.35)/.2))
 elif kind=='doors':
  opened=p.get('opened',False);reveal=p.get('reveal',False)
  for i,x in enumerate([270,540,810]):
   is_open=(i==2 and opened) or reveal
   d.rounded_rectangle((x-105,590,x+105,1050),12,fill=(50,39,24) if not is_open else (14,14,14),outline=G,width=6)
   d.polygon([(x-120,580),(x,500),(x+120,580)],outline=G,fill=(40,32,23))
   if is_open:
    if i==1:
     d.rounded_rectangle((x-75,800,x+75,860),12,fill=G);d.line((x-50,800,x-25,750,x+30,750,x+60,800),fill=WHITE,width=6)
     for z in [-45,45]:d.ellipse((x+z-20,840,x+z+20,880),fill=(15,15,15),outline=G,width=3)
    else:paste(c,asset('goat'),x,825,.24,0)
   else:
    d.rectangle((x-75,630,x+75,1000),outline=(180,140,65),width=3);text(c,str(i+1),800,FH,G,x=x)
   if i==0:d.line((x-100,1110,x+100,1110),fill=WHITE,width=7)
  fit(c,p.get('label','TON CHOIX'),1220,58)
 elif kind=='cases':
  text(c,'AU DÉPART',470,FL,G)
  for row,car in enumerate([0,1,2]):
   y=640+row*180
   for col in range(3):
    x=340+col*200;d.rounded_rectangle((x-75,y-50,x+75,y+50),10,fill=(125,91,33) if col==car else (38,32,25),outline=G,width=3);text(c,'AUTO' if col==car else 'CHÈVRE',y,font('Montserrat',30,'ExtraBold'),WHITE,x=x)
   text(c,'PERDU' if car==0 else 'GAGNÉ',y,font('Montserrat',34,'ExtraBold'),WHITE if car==0 else G,x=890)
  fit(c,'CHANGER GAGNE 2 FOIS SUR 3',1240,52)
 elif kind=='probability':
  text(c,'RESTER',570,FL,WHITE);text(c,'1 / 3',730,FN,WHITE);text(c,'CHANGER',990,FL,G);text(c,'2 / 3',1150,font('Playfair',190,'Black'),G)
 else:return False
 return True

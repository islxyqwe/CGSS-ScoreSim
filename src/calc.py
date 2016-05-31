# song=[[note= int(location in fraps)...],diffcultyrate,color=""(all,cute,cool,passion)]
# note=[[socre,happeningrate]...]
# bouns=[bounsrate,happeningrate]
# bounses=[bouns...]
# totalbouns=bouns(cbbouns*sbbouns)
import skill,unit
def samplesong():
	notes=[]
	for i in range(1,601):
		notes.append(i*12)
	return [notes,1.9,"all"]
def bounsappend(bounses,bounsrate,happeningrate):
	newrate=0
	for bouns in bounses:
		if bouns[0]<bounsrate:
			newrate+=bouns[1]*happeningrate
			bouns[1]-=bouns[1]*happeningrate
		if bouns[0]==bounsrate:
			bouns[1]+=newrate
			newrate=0
			break
	if newrate>0:
		bounses.append([bounsrate,newrate])
	bounses.sort(key=lambda x:x[0])
	return bounses
def calctotalbouns(bounses1,bounses2):
	totalbouns=[]
	for bounsl in bounses1:
		for bounsr in bounses2:
			totalbouns.append([bounsl[0]*bounsr[0],bounsl[1]*bounsr[1]])
	totalbouns.sort(key=lambda x:x[0])
	return totalbouns
def calcE(PDF):
	sum=0
	for x in PDF:
		sum+=x[0]*x[1]
	return sum
def calcEs(PDFs):
	res=[]
	for PDF in PDFs:
		res.append(calcE(PDF))
	return res
def PDF2CDF(PDF):
	CDF=[]
	sumrate=0
	for x in PDF:
		sumrate+=x[1]
		CDF.append([x[0],sumrate])
	return CDF
def CDF2PDF(CDF):
	PDF=[]
	sumrate=0
	for x in CDF:
		PDF.append([x[0],x[1]-sumrate])
		sumrate=x[1]
	return PDF
def calcmax(PDF,times):
	CDF=PDF2CDF(PDF)
	for x in CDF:
		x[1]=x[1]**times
	return CDF2PDF(CDF)
def bounsofnote(location,skills,songcolor):
	cbbouns=[[1,1]]
	sbbouns=[[1,1]]
	for skill in skills:
		if location%skill.interval<=skill.last:
			if skill.type:
				sbbouns=bounsappend(sbbouns,1+skill.effect/100,skill.getrate(songcolor)/100)
			else:
				cbbouns=bounsappend(cbbouns,1+skill.effect/100,skill.getrate(songcolor)/100)
	totalbouns=calctotalbouns(sbbouns,cbbouns)
	return totalbouns
def calcnotescore(standardscore,totalbouns,combobouns):
	note=[]
	for b in totalbouns:
		note.append([b[0]*standardscore*combobouns//1,b[1]])
	return note
def calcscore(song,unit):
	maxnote=len(song[0])
	standard=unit.appeal*song[1]/maxnote
	note=0
	combobouns=1
	notes=[]
	for n in song[0]:
		note+=1
		if note==maxnote//20:
			combobouns=1.1
		if note==maxnote//10:
			combobouns=1.2
		if note==maxnote//4:
			combobouns=1.3
		if note==maxnote//2:
			combobouns=1.4
		if note==int(maxnote*0.7):
			combobouns=1.5
		if note==int(maxnote*0.8):
			combobouns=1.7
		if note==int(maxnote*0.9):
			combobouns=2.0
		notes.append(calcnotescore(standard,bounsofnote(n,unit.skills,song[2]),combobouns))
	return notes
def anylizeskill(song,unit):
	bounses=[]
	for n in song[0]:
		bounses.append(bounsofnote(n,unit.skills,song[2]))
	return bounses
def calclive(song,unit,times):
	notes=calcscore(song,unit)
	avgscore=0
	avgmaxscore=0
	for n in notes:
		avgscore+=calcE(n)
		avgmaxscore+=calcE(calcmax(n,times))
	print("期望得分="+str(avgscore))
	print(str(times)+"次的期望最大得分="+str(avgmaxscore))
def skillcoverage(data):
	score=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	rating=[
	"无覆盖(F)","几乎无覆盖(E)","基本无覆盖(E+)",
	"非常差(D-)","差(D)","比较差(D+)",
	"略差(C-)","一般(C)","稍好(C+)",
	"比较良好(B-)","良好(B)","十分良好(B+)",
	"比较优秀(A-)","优秀(A)","十分优秀(A+)",
	"出色(S)","完美(SS)"
	]
	s=""
	for i in data:
		score[int((i-1)/0.02)]+=1
	for i in range(0,17):
		if score[i]>0:
			s=s+rating[i]+":"+str(score[i])+"("+str(int(100*score[i]/len(data)))+"%)\n"
	avg=sum(data)/len(data)
	s=s+"总评："+rating[int((avg-1)/0.02)]+"\n平均倍率:"+str(avg)
	return s
def plotdata(PDFs):
	i=0
	totalx=[]
	totaly=[]
	totalz=[]
	for PDF in PDFs:
		x=[]
		y=[]
		z=[]
		i+=1
		last=0
		CDF=PDF2CDF(PDF)
		for d in CDF:
			x.append(i)
			x.append(i)
			y.append(last)
			y.append(d[1])
			z.append(d[0])
			z.append(d[0])
			last=d[1]
		totalx.append(x)
		totaly.append(y)
		totalz.append(z)
	return [totalx,totaly,totalz]	
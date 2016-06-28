# song=[[note= int(location in fraps)...],diffcultyrate,color=""(all,cute,cool,passion)]
# note=[[socre,happeningrate]...]
# bouns=[bounsrate,happeningrate]
# bounses=[bouns...]
# totalbouns=bouns(cbbouns*sbbouns)
# num=[standard,numpyarray]
import skill,unit
import numpy as np
def fft_convolve(a,b):
    n = len(a)+len(b)-1
    N = 2**(int(np.log2(n))+1)
    A = np.fft.fft(a, N)
    B = np.fft.fft(b, N)
    return np.fft.ifft(A*B)[:n]
def convolve(a,b):
	return [a[0]+b[0],fft_convolve(a[1],b[1])]
def notes2numpyarray(notes):
	a=[]
	for n in notes:
		standard=int(min(n)[0])
		length=int(max(n)[0]-standard+1)
		temp=np.zeros(length)
		for b in n:
			temp[int(b[0]-standard)]+=b[1]
		a.append([standard,temp])
	return a
def sumscore(notes):
	a=notes2numpyarray(notes)
	sum=a[0]
	for i in range(1,len(a)):
		print(str(i)+"/"+str(len(a)-1))
		sum=convolve(sum,a[i])
	return sum
def numcalcE(a):
	length=len(a[1])
	sum=np.average(a[1],weights=np.arange(length)).real
	sum=a[0]+sum*length*(length-1)/2
	return sum
def numcalcmax(a,times):
	length=len(a[1])
	b=np.cumsum(a[1])
	b=b**times
	c=np.append(b[0],np.diff(b))
	return [a[0],c]
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
		if location%skill.interval<=skill.last and location>=skill.interval:
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
	standard=unit.appeal*float(song[1])/maxnote
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
		notes.append(calcnotescore(standard,bounsofnote(int(n),unit.skills,song[2]),combobouns))
	return notes
def anylizeskill(song,unit):
	bounses=[]
	for n in song[0]:
		bounses.append(bounsofnote(int(n),unit.skills,song[2]))
	return bounses
def anylyselive(song,unit):
	times=25
	notes=calcscore(song,unit)
	s=sumscore(notes)
	avgscore2=numcalcE(s)
	avgmaxscore=numcalcE(numcalcmax(s,25))
	minscore=s[0]
	maxscore=s[0]+len(s[1])-1
	t=np.cumsum(s[1])
	percent10=s[0]+np.where(t>0.1)[0][0]
	percent25=s[0]+np.where(t>0.25)[0][0]
	percent50=s[0]+np.where(t>0.5)[0][0]
	percent75=s[0]+np.where(t>0.75)[0][0]
	percent90=s[0]+np.where(t>0.9)[0][0]
	returnstr="期望得分="+str(avgscore2)+"\n"+str(times)+"次的期望最大得分="+str(avgmaxscore)
	returnstr=returnstr+"\n最小得分="+str(minscore)+"\n10%得分小于="+str(percent10)+"\n25%得分小于="+str(percent25)
	returnstr=returnstr+"\n50%得分小于="+str(percent50)+"\n75%得分小于="+str(percent75)
	returnstr=returnstr+"\n90%得分小于="+str(percent90)+"\n最高得分="+str(maxscore)
	return returnstr
def calclive(song,unit):
	avgscore=0
	notes=calcscore(song,unit)
	for n in notes:
		avgscore+=calcE(n)
	return "期望得分="+str(avgscore)
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
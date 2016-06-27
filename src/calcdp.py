import skill,unit
import numpy as np
# num=[standard,numpyarray]
def numsum(numleft,numright):
	if numleft[0]==0:
		return numright
	if numright[0]==0:
		return numleft
	if numleft[0]>numright[0]:
		lesser=numright
		higher=numleft
	else:
		lesser=numleft
		higher=numright
	standard=lesser[0]
	reformedhigher=np.append(np.zeros(higher[0]-lesser[0]),higher[1])
	if reformedhigher.size<lesser[1].size:
		reformedlesser=lesser[1]
		reformedhigher=np.append(reformedhigher,np.zeros(reformedlesser.size-reformedhigher.size))	
	else:
		reformedlesser=np.append(lesser[1],np.zeros(reformedhigher.size-lesser[1].size))
	result=reformedlesser+reformedhigher
	return [standard,result]
def getskillcount(location,skills):
	result=[]
	for skill in skills:
		result.append(location//skill.interval)
	return result
def getbouns(location,status,skills):
	cbbouns=1.0
	sbbouns=1.0
	for i in range(0,5):
		if status[i] and location%skills[i].interval<=skills[i].last:
			bouns=1+skills[i].effect/100
			if skills[i].type:
				if sbbouns<bouns:
					sbbouns=bouns
			else:
				if cbbouns<bouns:
					cbbouns=bouns
	return cbbouns*sbbouns
def calcnotescore(location,nowcount,skills,lastcount,laststatusno,combobouns,standardscore,songcolor):
	# nowcount=getskillcount(location,skills)
	laststatus=[]
	temp=laststatusno
	for i in range(0,5):
		laststatus.append(temp%2)
		temp=temp//2
	result=[[0,0]]*32
	statusrange=[]
	for i in range(0,5):
		if lastcount[i]==nowcount[i]:
			statusrange.append([laststatus[i]])
		else:
			statusrange.append([0,1])
	for ss0 in statusrange[0]:
		for ss1 in statusrange[1]:
			for ss2 in statusrange[2]:
				for ss3 in statusrange[3]:
					for ss4 in statusrange[4]:
						statusno=ss0+2*ss1+4*ss2+8*ss3+16*ss4
						ss=[ss0,ss1,ss2,ss3,ss4]
						prob=1.0
						for i in range(0,5):
							if lastcount[i]!=nowcount[i]:
								if ss[i]:
									prob=prob*skills[i].getrate(songcolor)/100
								else:
									prob=prob*(1-(skills[i].getrate(songcolor)/100))
						result[statusno]=[int(standardscore*combobouns*getbouns(location,ss,skills)),prob]
	return result
def calcscoresum(song,unit):
	maxnote=len(song[0])
	standard=unit.appeal*float(song[1])/maxnote
	skillcount=[-1,-1,-1,-1,-1]
	note=0
	combobouns=1
	score=[[0,np.array([1.0])]]+[[0,np.array([0.0])]]*31
	for n in song[0]:
		note+=1
		print(note)
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
		newscore=[[0,np.array([0.0])]]*32
		newskillcount=getskillcount(int(n),unit.skills)
		statusrange=[]
		for i in range(0,5):
			if skillcount[i]==newskillcount[i]:
				statusrange.append("no")
			else:
				statusrange.append("yes")
		for i in range(0,32):
			thenotescore=calcnotescore(int(n),newskillcount,unit.skills,skillcount,i,combobouns,standard,song[2])
			for j in range(0,32):
				if thenotescore[j][0]>0:
					temp=[score[i][0]+thenotescore[j][0],score[i][1]*thenotescore[j][1]]
					newscore[j]=numsum(newscore[j],temp)
		score=newscore
		skillcount=newskillcount
	result=score[0]
	for i in range(1,32):
		result=numsum(result,score[i])
	return result
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
def anylyselive(song,unit):
	times=25
	s=calcscoresum(song,unit)
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
import skill,unit
import numpy as np
# num=[standard,numpyarray]，f(S)=num[1][S-num[0]]
# 返回f',f'(s)=fl(s)+fr(s)
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
# 返回在location位置，对应的技能分别是第几个发动的技能
def getskillcount(location,skills):
	result=[]
	for skill in skills:
		result.append(location//skill.interval)
	return result
# 返回在location位置，某个状态status下分数的技能倍率
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
# result[statusno]=[S(location,laststatusno,statusno),F(location,laststatusno,statusno)]
# 即在location位置，上一个与现在的技能计数分别为lastcount，nowcount，
# 上一个状态是laststatusno，所有的技能为skills
# 基础分数为standardscore，歌曲颜色为songcolor，连击奖励为combobouns下
# 返回转移到各状态的对应得分以及概率
def calcnotescore(location,nowcount,skills,lastcount,laststatusno,combobouns,standardscore,songcolor):
	# nowcount=getskillcount(location,skills)
	# 从laststatusno分析laststatus下各技能的状态
	laststatus=[]
	temp=laststatusno
	for i in range(0,5):
		laststatus.append(temp%2)
		temp=temp//2
	result=[[0,0]]*32
	statusrange=[]
	for i in range(0,5):
		if lastcount[i]==nowcount[i]:# 如果计数值不变，这个技能的状态跟以前一样
			statusrange.append([laststatus[i]])
		else:# 如果计数值改变了，则这个技能的状态可能改变
			statusrange.append([0,1])
	# 此时statusrange为每个技能可能的状态
	for ss0 in statusrange[0]:
		for ss1 in statusrange[1]:
			for ss2 in statusrange[2]:
				for ss3 in statusrange[3]:
					for ss4 in statusrange[4]: # 遍历所有可能
						statusno=ss0+2*ss1+4*ss2+8*ss3+16*ss4 # 该可能的状态号
						ss=[ss0,ss1,ss2,ss3,ss4]
						prob=1.0
						for i in range(0,5):
							if lastcount[i]!=nowcount[i]:
								if ss[i]:
									prob=prob*skills[i].getrate(songcolor)/100 # 该技能发动的概率
								else:
									prob=prob*(1-(skills[i].getrate(songcolor)/100)) # 该技能没有发动的概率
						result[statusno]=[int(standardscore*combobouns*getbouns(location,ss,skills)),prob]
	return result
# 计算分数的概率质量函数并返回
def calcscoresum(song,unit):
	maxnote=len(song[0])
	standard=unit.appeal*float(song[1])/maxnote
	skillcount=[0,0,0,0,0]
	note=0
	combobouns=1
	score=[[0,np.array([1.0])]]+[[0,np.array([0.0])]]*31 # 初始状态
	print("calc PDF of score...")
	for n in song[0]: # 递推分数的概率质量函数
		note+=1
		print(str(note)+"/"+str(maxnote),end='\r')
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
		newscore=[[0,np.array([0.0])]]*32 # 保存新的概率质量函数
		newskillcount=getskillcount(int(n),unit.skills) #这个note的技能计数
		# statusrange=[]
		# for i in range(0,5):
			# if skillcount[i]==newskillcount[i]:
				# statusrange.append("no")
			# else:
				# statusrange.append("yes")
		for i in range(0,32): # 遍历旧的状态
			thenotescore=calcnotescore(int(n),newskillcount,unit.skills,skillcount,i,combobouns,standard,song[2])
			for j in range(0,32): # 在对应的终状态进行累加
				if thenotescore[j][0]>0:
					temp=[score[i][0]+thenotescore[j][0],score[i][1]*thenotescore[j][1]]
					newscore[j]=numsum(newscore[j],temp)
		score=newscore #保存概率质量函数和技能计数供下次递推使用
		skillcount=newskillcount
	result=score[0]
	for i in range(1,32): #把所有状态加起来
		result=numsum(result,score[i])
	print("Done.         ")
	return result
def numcalcE(a): #求期望值
	length=len(a[1])
	sum=np.average(a[1],weights=np.arange(length)).real #加权平均
	sum=a[0]+sum*length*(length-1)/2 #乘以总权值后加上偏移量
	return sum
def numcalcSD(a): #求标准差
	length=len(a[1])
	E=numcalcE(a)
	standarderror=a[0]-E
	myweights=np.arange(length)+standarderror
	myweights=myweights*myweights
	error=np.average(a[1],weights=myweights).real
	error=error*np.sum(myweights)
	result=np.sqrt(error)
	return result
def numcalcmax(a,times):
	length=len(a[1])
	b=np.cumsum(a[1]) #此时[a[0],b]为累计分布函数
	b=b**times #此时[a[0],b]为times后最大值的累计分布函数
	c=np.append(b[0],np.diff(b)) #此时[a[0],c]为[a[0],b]对应的概率质量函数
	return [a[0],c]
def anylyse(s):
	times=25
	avgscore2=numcalcE(s)
	error=numcalcSD(s)
	maxs=numcalcmax(s,times)
	avgmaxscore=numcalcE(maxs)
	errormax=numcalcSD(maxs)
	minscore=s[0]
	maxscore=s[0]+len(s[1])-1
	t=np.cumsum(s[1]) 
	percent10=s[0]+np.where(t>0.1)[0][0]
	percent25=s[0]+np.where(t>0.25)[0][0]
	percent50=s[0]+np.where(t>0.5)[0][0]
	percent75=s[0]+np.where(t>0.75)[0][0]
	percent90=s[0]+np.where(t>0.9)[0][0]
	percent99=s[0]+np.where(t>0.99)[0][0]
	returnstr="期望得分="+str(avgscore2)+"\n标准差:"+str(error)+"\n"+str(times)+"次的期望最大得分="+str(avgmaxscore)+"\n标准差:"+str(errormax)
	returnstr=returnstr+"\n最小得分="+str(minscore)+"\n10%得分小于="+str(percent10)+"\n25%得分小于="+str(percent25)
	returnstr=returnstr+"\n50%得分小于="+str(percent50)+"\n75%得分小于="+str(percent75)+"\n90%得分小于="+str(percent90)
	returnstr=returnstr+"\n99%得分小于="+str(percent99)+"\n最高得分="+str(maxscore)
	#returnstr=returnstr+str(np.nonzero(s[1]).size)
	return returnstr
def anylyselive(song,unit):
	s=calcscoresum(song,unit)
	return anylyse(s)
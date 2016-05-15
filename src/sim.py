import random,skill,unit
def simlive(unit):
	difficultybouns=1.9 #master 26
	maxnote=600
	note=0
	time=120*60 #fraps
	tap=time/maxnote
	standard=unit.appeal*difficultybouns/maxnote
	score=0
	combobouns=1.0
	for nowtime in range(0,time):
		sb=0
		cb=0
		for s in unit.skills:
			if nowtime%s.interval==0:
				if random.random()*100<s.rate:
					s.lasttime = s.last
			if s.lasttime>0:
				s.lasttime-=1
				if s.type:
					if s.effect>sb:
						sb=s.effect
				else:
					if s.effect>cb:
						cb=s.effect
		if nowtime==int(note*tap):
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
			score+=standard*(sb+100)*(cb+100)*combobouns//10000
	return score
def simlivetest(unit,times):
	ts=0
	bs=0
	for i in range(0,times):
		ns=simlive(unit)
		if ns>bs:
			bs=ns
		ts+=ns
	avg=ts//times
	#print("avg score=",avg)
	#print("best score=",bs)
	return bs
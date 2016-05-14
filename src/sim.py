import random,skill,unit
def simlive(unit):
	difficultybouns=1.9 #master 26
	note=600
	time=120*60 #fraps
	tap=time/note
	standard=unit.appeal*difficultybouns/note
	score=0
	combobouns=1.0
	for nowtime in range(0,time-1):
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
		if nowtime%tap==0:
			score+=standard*(sb+100)*(cb+100)*combobouns//10000
			note-=1
			if note==570:
				combobouns=1.1
			if note==540:
				combobouns=1.2
			if note==450:
				combobouns=1.3
			if note==300:
				combobouns=1.4
			if note==180:
				combobouns=1.5
			if note==120:
				combobouns=1.7
			if note==60:
				combobouns=2.0
	return score
def simlivetest(unit,times):
	ts=0
	bs=0
	for i in range(1,times):
		ns=simlive(unit)
		if ns>bs:
			bs=ns
		ts+=ns
	avg=ts//times
	print("avg score=",avg)
	print("best score=",bs)
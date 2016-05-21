import sys,getopt,csv,random,math,skill,unit,sim
def randomdata():
	s=[str(random.randint(100000,300000))]
	for i in range(0,5):
		t=random.randint(0,1)
		r=random.randint(2,3)
		interval=[4,6,7,9,11]
		if r==3:
			interval.append(13)
		i=random.choice(interval)
		if r==2:
			l=math.ceil(i/2)
		else:
			l=i//2
		if t==0:
			e=random.choice([12,15])
		else:
			e=random.choice([15,17])
		#lv=random.randint(1,10)
		lv=max(random.randint(5,10),random.randint(5,10),random.randint(5,10),random.choice([5,10]))
		s.extend([str(t),str(i),str(l),str(e),str(lv),str(r)])
	return s
def main(argv):
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"ho:t:",["ofile=","time="])
	except getopt.GetoptError:
		print('createinput.py -t times -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('createinput.py -t times -o <outputfile>')
			sys.exit()
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-t", "--time"):
			time = arg
	fo = open (outputfile, "wt", newline='')
	writer = csv.writer(fo,dialect='excel')
	for i in range(0,int(time)):
		r=randomdata()
		s1=skill.skill(r[1],r[2],r[3],r[4],r[5],r[6])
		s2=skill.skill(r[7],r[8],r[9],r[10],r[11],r[12])
		s3=skill.skill(r[13],r[14],r[15],r[16],r[17],r[18])
		s4=skill.skill(r[19],r[20],r[21],r[22],r[23],r[24])
		s5=skill.skill(r[25],r[26],r[27],r[28],r[29],r[30])
		u=unit.unit(int(r[0]),[s1,s2,s3,s4,s5])
		s=0
		for j in range (0,25):
			s+=int(sim.simlivetest(u,25))
		s=s//25
		r.append(str(s))
		writer.writerow(r)
		print(i+1,"/",time)
	fo.close()
	
if __name__ == "__main__":
	main(sys.argv[1:])

import sys,getopt,csv,random,math
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
		lv=random.randint(1,10)
		s.extend([str(t),str(i),str(l),str(e),str(lv),str(r)])
	return s
def main(argv):
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"ho:t:",["ofile="])
	except getopt.GetoptError:
		print('createinput.py -t times -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('createinput.py -t times -o <outputfile>')
			sys.exit()
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-t"):
			time = arg
	fo = open (outputfile, "wt", newline='')
	writer = csv.writer(fo,dialect='excel')
	for i in range(0,int(time)):
		writer.writerow(randomdata())
	fo.close()
	
if __name__ == "__main__":
	main(sys.argv[1:])

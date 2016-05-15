import sim,skill,unit,sys,getopt,csv
def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('do.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('do.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	fi = open(inputfile, "rt")
	reader = csv.reader(fi)
	fo = open (outputfile, "wt", newline='')
	writer = csv.writer(fo,dialect='excel')
	i=0
	for r in reader:
		s1=skill.skill(r[1],r[2],r[3],r[4],r[5],r[6])
		s2=skill.skill(r[7],r[8],r[9],r[10],r[11],r[12])
		s3=skill.skill(r[13],r[14],r[15],r[16],r[17],r[18])
		s4=skill.skill(r[19],r[20],r[21],r[22],r[23],r[24])
		s5=skill.skill(r[25],r[26],r[27],r[28],r[29],r[30])
		u=unit.unit(int(r[0]),[s1,s2,s3,s4,s5])
		r.append(str(int(sim.simlivetest(u,25))))
		writer.writerow(r)
		i+=1
		print(i)
	fi.close()
	fo.close()
if __name__ == "__main__":
	main(sys.argv[1:])
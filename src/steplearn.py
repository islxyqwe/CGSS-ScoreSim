import createinput,skill,unit,sim,sys,getopt
import neurolab as nl
import numpy as np
from sklearn import preprocessing
def main(argv):
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"ht:",["time="])
	except getopt.GetoptError:
		print('createinput.py -t times')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('createinput.py -t times')
			sys.exit()
		elif opt in ("-t", "--time"):
			time = arg
	s=np.loadtxt(".\\nn\\scaler", delimiter=",")
	scalera = preprocessing.StandardScaler()
	scalerb = preprocessing.MinMaxScaler(feature_range=(-1, 1))
	scalera.scale_=s[0]
	scalera.mean_=s[1]
	scalerb.scale_=s[2]
	scalerb.min_=s[3]
	net = nl.load(".\\nn\\brain")
	for i in range(0,int(time)):
		inp=[]
		tar=[]
		for j in range(0,10):
			r=createinput.randomdata()
			s1=skill.skill(r[1],r[2],r[3],r[4],r[5],r[6])
			s2=skill.skill(r[7],r[8],r[9],r[10],r[11],r[12])
			s3=skill.skill(r[13],r[14],r[15],r[16],r[17],r[18])
			s4=skill.skill(r[19],r[20],r[21],r[22],r[23],r[24])
			s5=skill.skill(r[25],r[26],r[27],r[28],r[29],r[30])
			u=unit.unit(int(r[0]),[s1,s2,s3,s4,s5])
			s=int(sim.simlivetest(u,25))
			inp.append(r)
			tar.append([(s-500000)/1000000])
		inp=scalerb.transform(scalera.transform(inp))
		net.train(inp, tar, epochs=1, show=1, goal=0)
		print(i+1,"/",time)
	net.save(".\\nn\\brain")
if __name__ == "__main__":
	main(sys.argv[1:])
import numpy as np
import neurolab as nl
from sklearn import preprocessing
import sys,getopt,math
def main(argv):
	trainset = ''
	testset = ''
	try:
		opts, args = getopt.getopt(argv,"ha:b:",["trainfile=","testfile="])
	except getopt.GetoptError:
		print('train.py -a <trainsetfile> -b <testsetfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('train.py -a <trainsetfile> -b <testsetfile>')
			sys.exit()
		elif opt in ("-a","--trainfile"):
			trainset = arg
		elif opt in ("-b","--testfile"):
			testset = arg
	dataset=np.loadtxt(trainset, delimiter=",")
	x=dataset[:,0:31]
	size=len(x)
	y=(dataset[:,31]).reshape(size,1)
	tar=(y-500000)/1000000
	scalera = preprocessing.StandardScaler().fit(x)
	tmp = scalera.transform(x)  
	scalerb = preprocessing.MinMaxScaler(feature_range=(-1, 1)).fit(tmp)
	inp = scalerb.transform(tmp)
	
	form=[]
	for i in range(0,31):
		form.append([-1,1])
	
	net = nl.net.newff(form,[60,30,1])
	
	testset=np.loadtxt(testset, delimiter=",")
	xt=testset[:,0:31]
	sizet=len(xt)
	testinp=scalerb.transform(scalera.transform(xt))
	yt=(testset[:,31]).reshape(sizet,1)
	testtar=(yt-500000)/1000000
	
	net.train(inp, tar, epochs=700, show=50, goal=0.01)
	# 
	# errortrain=[]
	# errortest=[]
	# for i in range(0,40):
		# net.train(inp, tar, epochs=30, show=15, goal=0.001)
		# out = net.sim(inp)
		# res = out*1000000+500000
		# errortrain.append(err(y,res))
		# out = net.sim(testinp)
		# res = out*1000000+500000
		# errortest.append(err(yt,res))
	# import matplotlib.pyplot as pl
	# pl.subplot(211)
	# pl.plot(errortrain)
	# pl.xlabel('Epoch number')
	# pl.ylabel('error (trainset)')
	# pl.subplot(212)
	# pl.plot(errortest)
	# pl.xlabel('Epoch number')
	# pl.ylabel('error (testset)')
	# pl.show()
	#
	err=nl.error.MSE()
	out = net.sim(inp)
	res = out*1000000+500000
	np.savetxt("traindataoutput.csv", res, delimiter=",")
	print("training err",math.sqrt(err(res,y)))
	out = net.sim(testinp)
	res = out*1000000+500000
	print("testing err",math.sqrt(err(res,yt)))
	np.savetxt("testdataoutput.csv", res, delimiter=",")
	np.savetxt(".\\nn\\scaler", [scalera.scale_,scalera.mean_,scalerb.scale_,scalerb.min_], delimiter=",")
	net.save(".\\nn\\brain")
	
	
if __name__ == "__main__":
	main(sys.argv[1:])
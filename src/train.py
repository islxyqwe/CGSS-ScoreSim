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
	
	form=[]	#输入数据的结构
	for i in range(0,31):
		form.append([-1,1]) #每个输入数据的范围
	
	net = nl.net.newff(form,[10,1]) 	#设定神经网结构，[6,1] 单隐层，隐藏层6个输出层1个
										#[12,12,1] 双隐层，第一隐藏层12个第二隐藏层12个输出层1个
										#复杂的网络容易发生过拟合，简单的容易欠拟合，层数多的难以训练
										#数据越多，过拟合更难发生，但是运算时间会增加
	testset=np.loadtxt(testset, delimiter=",")
	xt=testset[:,0:31]
	sizet=len(xt)
	testinp=scalerb.transform(scalera.transform(xt))
	yt=(testset[:,31]).reshape(sizet,1)
	testtar=(yt-500000)/1000000
	
	goal=3000 #goal: 目标误差。设定过大会欠拟合，过小容易过拟合。
	goalerr=(goal/1414213)**2*size
	print("goal =",goal,"SSE = ",goalerr)
	net.train(inp, tar, epochs=3000, show=50, goal=goalerr, rr=1/15) 
	err=nl.error.MSE()
	
	# errortrain=[]
	# errortest=[]
	# for i in range(0,400):
		# net.train(inp, tar, epochs=5, show=5, goal=0.003)
		# out = net.sim(inp)
		# res = out*1000000+500000
		# errortrain.append(math.sqrt(err(res,y)))
		# out = net.sim(testinp)
		# res = out*1000000+500000
		# errortest.append(math.sqrt(err(res,yt)))
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
	# 显示学习曲线的代码，设定目标误差用
	
	out = net.sim(inp)
	res = out*1000000+500000
	np.savetxt("traindataoutput.csv", res, delimiter=",")
	print("training err",math.sqrt(err(res,y)))#本身误差和测试误差都很大，则发生了欠拟合
	out = net.sim(testinp)
	res = out*1000000+500000
	print("testing err",math.sqrt(err(res,yt)))#测试数据的误差大很多，则发生了过拟合
	np.savetxt("testdataoutput.csv", res, delimiter=",")
	np.savetxt(".\\nn\\scaler", [scalera.scale_,scalera.mean_,scalerb.scale_,scalerb.min_], delimiter=",")
	net.save(".\\nn\\brain")
	
	
if __name__ == "__main__":
	main(sys.argv[1:])
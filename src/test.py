import neurolab as nl
import numpy as np
from sklearn import preprocessing
import skill,unit,csv,sim,math
s=np.loadtxt(".\\nn\\scaler", delimiter=",")
scalera = preprocessing.StandardScaler()
scalerb = preprocessing.MinMaxScaler(feature_range=(-1, 1))
scalera.scale_=s[0]
scalera.mean_=s[1]
scalerb.scale_=s[2]
scalerb.min_=s[3]
net = nl.load(".\\nn\\brain")

testset=np.loadtxt("highlvtest.csv", delimiter=",")

# fi = open ("highlvtest.csv", "rt")
# reader = csv.reader(fi,dialect='excel')
# fo = open ("testdata2.csv", "wt", newline='')
# writer = csv.writer(fo,dialect='excel')
# i=0
# for r in reader:
	# print(r)
	# s1=skill.skill(r[1],r[2],r[3],r[4],r[5],r[6])
	# s2=skill.skill(r[7],r[8],r[9],r[10],r[11],r[12])
	# s3=skill.skill(r[13],r[14],r[15],r[16],r[17],r[18])
	# s4=skill.skill(r[19],r[20],r[21],r[22],r[23],r[24])
	# s5=skill.skill(r[25],r[26],r[27],r[28],r[29],r[30])
	# u=unit.unit(int(r[0]),[s1,s2,s3,s4,s5])
	# s=str(int(sim.simlivetest(u,25)))
	# writer.writerow([s])
	# i+=1
	# print(i)
# fi.close()
# fo.close()
xt=testset[:,0:31]
sizet=len(xt)
testinp=scalerb.transform(scalera.transform(xt))
yt=(testset[:,31]).reshape(sizet,1)
testtar=(yt-500000)/1000000

out=net.sim(testinp)*1000000+500000
err=nl.error.MSE()
print("testing err",math.sqrt(err(out,yt)))
np.savetxt("testdata.csv", out, delimiter=",")
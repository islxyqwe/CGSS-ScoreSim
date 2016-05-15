import neurolab as nl
import numpy as np
from sklearn import preprocessing
import skill,unit
def simlivenn(unit):
	s=np.loadtxt(".\\nn\\scaler", delimiter=",")
	scalera = preprocessing.StandardScaler()
	scalerb = preprocessing.MinMaxScaler(feature_range=(-1, 1))
	scalera.scale_=s[0]
	scalera.mean_=s[1]
	scalerb.scale_=s[2]
	scalerb.min_=s[3]
	net = nl.load(".\\nn\\brain")
	inp=[unit.appeal]
	for s in unit.skills:
		inp.extend(s.array)
	inp=scalerb.transform(scalera.transform([inp]))  
	out=net.sim(inp)*1000000+500000
	return int(out[0][0])
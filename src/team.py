import unit,centerskill,idol
def calcbackappeal(idols,buff):
	appeal=0
	buffedidols=[]
	for i in idols:
		buffedidols.append(idol.idol(i.name,i.skill,i.centerskill,i.vo*getattr(buff,i.type+"vo")//200,i.vi*getattr(buff,i.type+"vi")//200,i.da*getattr(buff,i.type+"da")//200,i.type,i.life))
	buffedidols.sort(lambda a,b:b.appeal-a.appeal)
	for j in range(0,10):
		appeal+=buffedidols[j].appeal
	return appeal
class team:
	def __init__(self,idols,guest,backappeal,buff,cubuff,cobuff,pabuff):
		self.vo=0
		self.vi=0
		self.da=0
		self.life=0
		self.appeal=backappeal
		totalbuff = idols[0].centerskill+guest.centerskill+buff+cubuff+cobuff+pabuff+centerskill.centerskill("all","all",100)
		self.skills=[]
		for i in idols:
			self.vo+=i.vo*getattr(totalbuff,i.type+"vo")//100
			self.vi+=i.vi*getattr(totalbuff,i.type+"vi")//100
			self.da+=i.da*getattr(totalbuff,i.type+"da")//100
			self.life+=i.life*getattr(totalbuff,i.type+"life")//100
			self.skills.append(i.skill)
		self.vo+=guest.vo*getattr(totalbuff,guest.type+"vo")//100
		self.vi+=guest.vi*getattr(totalbuff,guest.type+"vi")//100
		self.da+=guest.da*getattr(totalbuff,guest.type+"da")//100
		self.life+=guest.life*getattr(totalbuff,i.type+"life")//100
		self.appeal+=self.vo+self.vi+self.da+18 #6*3
		self.unit=unit.unit(self.appeal,self.skills)

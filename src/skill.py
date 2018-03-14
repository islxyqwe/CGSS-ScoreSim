class skill:
	def __init__(self, type, interval, last, effect, level, rate):
		self.type = int(type) # 0 sb 1 cb
		self.interval = int(interval)*60
		self.last = int(last)*60*(1+0.054*(int(level)-1))
		self.effect = int(effect)
		self.rate = (25+5*int(rate))*(1+0.054*(int(level)-1))
		self.lasttime = 0
		self.level=level
		self.array=[type, interval, last, effect, level, rate]
		self.color=""
	def getrate(self,color):
		if color==self.color or color=="all":
			return self.rate*1.3
		elif color=="plus":
			return self.rate*1.3*1.2
		else:
			return self.rate
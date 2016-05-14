class skill:
	def __init__(self, type, interval, last, effect, level, rate):
		self.type = type # 0 sb 1 cb
		self.interval = int(interval)*60
		self.last = int(last)*60*(1+0.054*(int(level)-1))
		self.effect = int(effect)
		self.rate = (30+5*int(rate))*(1+0.054*(int(level)-1))*1.3
		self.lasttime = 0
class skill:
	def __init__(self, type, interval, last, effect, level, rate):
		self.type = type # 0 sb 1 cb
		self.interval = interval*60
		self.last = last*60*(1+0.054*(level-1))
		self.effect = effect
		self.rate = (30+5*rate)*(1+0.054*(level-1))*1.3
		self.lasttime = 0
import skill,centerskill
class idol:
	def __init__(self, name, skill, centerskill, vo, da, vi, type, life):
		self.name = name
		self.skill = skill
		self.vo = vo
		self.vi = vi
		self.da = da
		self.type = type
		self.centerskill = centerskill
		self.life = life
		self.appeal=vo+vi+da
		self.skill.color=type
		return self.name+"("+str(self.appeal)+")"
def newidol(a):
	return i
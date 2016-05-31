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
	def __str__(self):
		return self.name+"("+str(self.appeal)+")"
def newidol(a):
	i=idol(a[0],skill.skill(int(a[1]),int(a[2]),int(a[3]),int(a[4]),int(a[5]),int(a[6])),centerskill.centerskill(a[7],a[8],int(a[9])),int(a[10]),int(a[11]),int(a[12]),a[13],int(a[14]))
	return i
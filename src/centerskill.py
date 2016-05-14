class centerskill:
	def __init__(self, type, target, effect):
		a=["cu","co","pa"]
		b=["vo","vi","da","skill","life"]
		for c in a:
			for d in b:
				if (c==type or type=="all") and (d==target or (target=="appeal"and d in ["vo","vi","da"]) or target=="all"):
						setattr(self,c+d,effect)
				else:
					setattr(self,c+d,0)
	def __add__(self, other):
		n=centerskill("","",0)
		a=["cu","co","pa"]
		b=["vo","vi","da","skill","life"]
		for c in a:
			for d in b:
					setattr(n,c+d,getattr(self,c+d)+getattr(other,c+d))
		return n
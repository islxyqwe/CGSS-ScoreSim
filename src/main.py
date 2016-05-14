import sim,skill,unit
low=1
med=2
high=3
cb=0
sb=1
s1=skill.skill(cb,6,3,12,10,med)
s2=skill.skill(sb,9,5,15,10,med)
s3=skill.skill(cb,11,5,15,10,high)
s4=skill.skill(sb,13,6,17,10,high)
s5=skill.skill(sb,7,4,15,10,med)
u=unit.unit(288017,[s1,s2,s3,s4,s5])
#u=unit.unit(290174,[s1,s2,s3,s4])
sim.simlivetest(u,200)
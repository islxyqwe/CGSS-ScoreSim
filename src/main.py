import sim,skill,unit,centerskill,idol,team
import nn
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
i1=idol.idol("mio",s1,centerskill.centerskill("all","vo",48),6115,3854,3137,"pa",39)
i2=idol.idol("natalia",s2,centerskill.centerskill("pa","vo",60),6008,2991,3707,"pa",39)
i3=idol.idol("airi",s3,centerskill.centerskill("pa","vo",90),6954,4564,3779,"pa",44)
i4=idol.idol("aiko",s4,centerskill.centerskill("pa","vo",90),6982,4596,3812,"pa",44)
i5=idol.idol("mika",s5,centerskill.centerskill("pa","vo",60),5729,3166,3806,"pa",39)
songbouns=centerskill.centerskill("all","appeal",30)+centerskill.centerskill("all","skill",30)
cubouns=centerskill.centerskill("cu","appeal",10)
cobouns=centerskill.centerskill("co","appeal",10)
pabouns=centerskill.centerskill("pa","appeal",10)
t=team.team([i3,i2,i4,i1,i5],i4,99798,songbouns,cubouns,cobouns,pabouns)
u=t.unit
#u=unit.unit(288017,[s1,s2,s3,s4,s5])
print(nn.simlivenn(u))
print(sim.simlivetest(u,25))
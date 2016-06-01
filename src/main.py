import skill,unit,centerskill,idol,team
import calc,csv
import _thread

# low=1
# med=2
# high=3
# cb=0
# sb=1
# s1=skill.skill(cb,6,3,12,10,med)
# s2=skill.skill(sb,9,5,15,10,med)
# s3=skill.skill(cb,11,5,15,10,high)
# s4=skill.skill(sb,13,6,17,10,high)
# s5=skill.skill(sb,7,4,15,10,med)
# s6=skill.skill(cb,13,6,12,10,high)
# i1=idol.idol("mio",s1,centerskill.centerskill("all","vo",48),6115,3137,3854,"pa",39)
# i2=idol.idol("natalia",s2,centerskill.centerskill("pa","vo",60),6008,3707,2991,"pa",39)
# i3=idol.idol("airi",s3,centerskill.centerskill("pa","vo",90),6954,3779,4564,"pa",44)
# i4=idol.idol("aiko",s4,centerskill.centerskill("pa","vo",90),6982,3812,4596,"pa",44)
# i5=idol.idol("mika",s5,centerskill.centerskill("pa","vo",60),5729,3806,3166,"pa",39)
# i6=idol.idol("kaoru",s6,centerskill.centerskill("pa","vo",60),6061,3228,3921,"pa",39)
# idols=[i1,i2,i3,i4,i5,i6]
idols=[]
with open('idols.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		idols.append(idol.newidol(row))
songs=[]
with open('songs.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		songs.append([row[0],row[3:],row[2],row[1]])
with open('last.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		setting=row

cubouns=centerskill.centerskill("cu","appeal",10)
cobouns=centerskill.centerskill("co","appeal",10)
pabouns=centerskill.centerskill("pa","appeal",10)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
def createteam(*args):
	idolteam=[]
	for i in range(0,6):
		s=myteam[i].get()
		idolteam.append(idols[int(s[0:s.index('.')])-1])
	s=mysong.get()
	song=songs[int(s[0:s.index('.')])-1]
	song=song[1:]
	songbouns=centerskill.centerskill(song[2],"appeal",30)+centerskill.centerskill(song[2],"skill",30)
	u=team.team(idolteam[:5],idolteam[5],int(backappeal.get()),songbouns,cubouns,cobouns,pabouns).unit
	comment.set("总APPEAL值="+str(u.appeal))
def calcprepare():
	idolteam=[]
	for i in range(0,6):
		s=myteam[i].get()
		idolteam.append(idols[int(s[0:s.index('.')])-1])
	s=mysong.get()
	song=songs[int(s[0:s.index('.')])-1]
	song=song[1:]
	songbouns=centerskill.centerskill(song[2],"appeal",30)+centerskill.centerskill(song[2],"skill",30)
	u=team.team(idolteam[:5],idolteam[5],int(backappeal.get()),songbouns,cubouns,cobouns,pabouns).unit
	return [song,u]
def calcresult(*args):
	data=calcprepare()
	s=calc.calclive(data[0],data[1])
	notebouns=calc.anylizeskill(data[0],data[1])
	res=calc.calcEs(notebouns)
	s=s+"\n技能分析：\n"+calc.skillcoverage(res)
	messagebox.showinfo('计算结果', s)
def anylyse(*args):
	data=calcprepare()
	pro.start()
	s=_thread.start_new_thread(anylysetheard,(data[0],data[1],pro,) )
def anylysetheard(song,unit,pro):
	s=calc.anylyselive(song,unit)
	pro.stop()
	messagebox.showinfo('计算结果', s)
root=tk.Tk()
root.title("CGSS分数计算器&技能分析")
root.resizable(width=False, height=False)
selection=[]
seq=0
for i in idols:
	seq+=1
	selection.append(str(seq)+"."+str(i))
songselection=[]
seq=0
for s in songs:
	seq+=1
	songselection.append(str(seq)+"."+s[0]+","+str(int(len(s[1])))+"notes")
myteam=[]
for i in range(0,6):
	myteam.append(tk.StringVar())
	myteam[i].set(selection[int(setting[1+i])])
	myteam[i].trace("w",createteam)
mysong=tk.StringVar()
mysong.set(songselection[int(setting[0])])
mysong.trace("w",createteam)
tk.Label(root,text='歌曲').pack()
ttk.Combobox(root,text=mysong,values=songselection,width=50,state='readonly').pack()
tk.Label(root,text='Center偶像').pack()
ttk.Combobox(root,text=myteam[0],values=selection,width=50,state='readonly').pack()
tk.Label(root,text='队伍偶像').pack()
for i in range(1,5):
	ttk.Combobox(root,text=myteam[i],values=selection,width=50,state='readonly').pack()
tk.Label(root,text='GUEST偶像').pack()
ttk.Combobox(root,text=myteam[5],values=selection,width=50,state='readonly').pack()
tk.Label(root,text='后援APPEAL值').pack()
backappeal=tk.StringVar()
backappeal.set(setting[7])
backappeal.trace("w",createteam)
tk.Entry(root,text=backappeal).pack()
comment=tk.StringVar()
comment.set("总APPEAL值=")
createteam()
tk.Label(root,textvariable=comment).pack()
tk.Button(root,text='计算期望与技能覆盖',command=calcresult,activeforeground='white',activebackground='red').pack()
tk.Button(root,text='分析得分分布情况（警告：慢）',command=anylyse,activeforeground='white',activebackground='red').pack()
pro=ttk.Progressbar(root)
pro.pack()
root.mainloop()
with open('last.csv','w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	s=mysong.get()
	towrite=[str(int(s[0:s.index('.')])-1)]
	for i in range(0,6):
		s=myteam[i].get()
		towrite.append(str(int(s[0:s.index('.')])-1))
	towrite.append(backappeal.get())
	writer.writerow(towrite)


# t=team.team([i3,i2,i4,i6,i1],i4,99798,songbouns,cubouns,cobouns,pabouns)
# u=t.unit
# u=unit.unit(294969,[s6,s7,s8,s9,s10])
# calc.calclive(calc.samplesong(),u,25)
# notebouns=calc.anylizeskill(calc.samplesong(),u)
# res=calc.calcEs(notebouns)
# print("技能分析：")
# print(calc.skillcoverage(res))
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# res=calc.plotdata(notebouns)
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# for i in range(0,len(res[0])):
	# ax.plot(res[0][i], res[1][i], res[2][i], label='parametric curve')
# plt.show()
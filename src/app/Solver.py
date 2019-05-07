from anastruct import SystemElements
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import os
def unique_by_first_n(n, coll):
    seen = set()
    for item in coll:
        compare = tuple(item[:n])    # Keep only the first `n` elements in the set
        if compare not in seen:
            seen.add(compare)
            yield item

ss = SystemElements(EA=5000)

####input
str1=sys.argv[1]
str2=sys.argv[2]

forces=str2.split(',')

list11=[]
temp=[]
strr=str1.split(';')
strr.pop()
for i in strr:
    temp=i.split(',')
    list11.append(temp)
forces.pop()
#draw member
if(os.stat("src/app/guru99.txt").st_size != 0):
  lines = np.loadtxt('src/app/guru99.txt', dtype=np.object)
  lines = lines.tolist()
#################


##############
joints =list11
new_id=[]
for line in lines :
   ss.add_truss_element(location=[joints[int(line[0])], joints[int(line[1])]])
   new_id.append(int(line[0]))
   new_id.append(int(line[1]))
#print(new_id)
list1=list(dict.fromkeys(new_id))
#print(list1)

#draw supports
if(os.stat("src/app/supports.txt").st_size != 0):
   supports = np.loadtxt('src/app/supports.txt', dtype=np.object)#read from files
   supports = supports.tolist()
   for support in supports:

      ss.add_support_hinged(node_id=1 + list1.index((int(support))))

#draw v_loads
f=0
if(os.stat("src/app/v_loads.txt").st_size != 0):
 v_loads = np.loadtxt('src/app/v_loads.txt', dtype=np.object)#read from files
 v_loads  = v_loads .tolist()
 for v in v_loads:
    ss.point_load(Fx=int(forces[f]), node_id=1 + list1.index((int(v))))
    f=f+1
#draw h_loads
if(os.stat("src/app/h_loads.txt").st_size != 0):
 h_loads = np.loadtxt('src/app/h_loads.txt', dtype=np.object)#read from files
 h_loads  = h_loads .tolist()
 for h in h_loads:
    ss.point_load(Fy=int(forces[f]), node_id=1 + list1.index((int(h))),rotation=180)
    f=f+1
fig = ss.show_structure(show=True)
plt.title('A sine wave')
plt.savefig('src/app/my-figure.png')

ss.solve(show=True)
ss.show_reaction_force(show=True)
ss.show_axial_force(show=True)
ss.show_displacement(factor=10)
ss.show_bending_moment(show=True)
sys.stdout.flush()

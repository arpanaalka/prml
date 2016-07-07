import numpy as np
import random
import math

eta=0.1
s=0.003 # 3ms transmission time b/w any two nodes
eps=np.exp(-3)
dest=8
Qgrid=[]
Qmatrix=np.zeros(shape=(3,4))

'''
grid structure is as shown below

		1----2     3----4
		|		|
		|		|
		5----6-----7----8
		|		|
		|		|
		9---10----11---12

'''

class Node:

	def __init__(self,no):
		self.no=no
		self.adj_nodes=np.zeros(3,dtype=np.int)
		self.adj_costs=np.zeros(3)
		self.q=np.random.uniform(0,1,12)+10
		self.q[no-1]=0.0
		self.qDelay=np.random.uniform(0,1)


for i in range(0,12):
	Qgrid.append(Node(i+1))


#build the above topology of nodes
Qgrid[0].adj_nodes=np.copy(np.array([2,5,0]))
Qgrid[0].q[1]=1
Qgrid[0].q[4]=1
Qgrid[0].adj_costs=np.copy(np.array([0,0,-1.0]))

Qgrid[1].adj_nodes=np.copy(np.array([1,0,0]))
Qgrid[1].q[0]=1
Qgrid[1].adj_costs=np.copy(np.array([0,-1.0,-1.0]))

Qgrid[2].adj_nodes=np.copy(np.array([4,0,0]))
Qgrid[2].q[3]=1
Qgrid[2].adj_costs=np.copy(np.array([0,-1.0,-1.0]))

Qgrid[3].adj_nodes=np.copy(np.array([3,8,0]))
Qgrid[3].q[2]=1
Qgrid[3].q[7]=1
Qgrid[3].adj_costs=np.copy(np.array([0,0,-1.0]))

Qgrid[4].adj_nodes=np.copy(np.array([1,6,9]))
Qgrid[4].q[0]=1
Qgrid[4].q[5]=1
Qgrid[4].q[8]=1
Qgrid[4].adj_costs=np.copy(np.array([0,0,0.]))

Qgrid[5].adj_nodes=np.copy(np.array([5,7,0]))
Qgrid[5].q[4]=1
Qgrid[5].q[6]=1
Qgrid[5].adj_costs=np.copy(np.array([0,0,-1.0]))

Qgrid[6].adj_nodes=np.copy(np.array([6,8,0]))
Qgrid[6].q[5]=1
Qgrid[6].q[7]=1
Qgrid[6].adj_costs=np.copy(np.array([0,0,-1.0]))

Qgrid[7].adj_nodes=np.copy(np.array([4,7,12]))
Qgrid[7].q[3]=1
Qgrid[7].q[6]=1
Qgrid[7].q[11]=1
Qgrid[7].adj_costs=np.copy(np.array([0,0,0.]))

Qgrid[8].adj_nodes=np.copy(np.array([5,10,0]))
Qgrid[8].q[4]=1
Qgrid[8].q[9]=1
Qgrid[8].adj_costs=np.copy(np.array([0,0,-1.0]))

Qgrid[9].adj_nodes=np.copy(np.array([9,11,0]))
Qgrid[9].q[8]=1
Qgrid[9].q[10]=1
Qgrid[9].adj_costs=np.copy(np.array([0,0,-1.0]))

Qgrid[10].adj_nodes=np.copy(np.array([10,12,0]))
Qgrid[10].q[9]=1
Qgrid[10].q[11]=1
Qgrid[10].adj_costs=np.copy(np.array([0,0,-1.0]))

Qgrid[11].adj_nodes=np.copy(np.array([8,11,0]))
Qgrid[11].q[7]=1
Qgrid[11].q[10]=1
Qgrid[11].adj_costs=np.copy(np.array([0,0,-1.0]))

episode=0
counter=0
old_next_list=np.zeros(12,dtype=np.int)
new_next_list=np.zeros(12,dtype=np.int)
while True:
	#set destination here to variable dest

	for i in range(0,12):
		adj=[]
		adj=np.copy(Qgrid[i].adj_nodes)
		indx=0
		dest_cost=[]
		while adj[indx]!=0 and indx<4:
			dest_cost.append(Qgrid[adj[indx]-1].q[dest-1])
			indx=indx+1
			if indx==3:
				break
			#print ('%d %d\n' %(i,indx))

		#select the next node to forward the packet GREEDILY	
		indx=np.argmin(dest_cost)	
		next=adj[indx]-1
		new_next_list[i]=next
		minNext=Qgrid[next].q[dest-1]
		deltaQ=eta*(Qgrid[i].qDelay+s+minNext - Qgrid[i].q[dest-1])	
		Qgrid[i].q[dest-1]=Qgrid[i].q[dest-1]+deltaQ

	if(np.linalg.norm(new_next_list-old_next_list)<eps):
		counter=counter+1
	else:
		counter=0

	if counter>10:
		break	
	episode=episode+1
	if episode>100:
		break
	old_next_list=np.copy(new_next_list)	

print('final route to destination %d\n' %dest)
for i in range(0,12):
	if(i+1==dest):
		continue
	print('next node for [%d] :%d\n'%(i+1,new_next_list[i]+1))


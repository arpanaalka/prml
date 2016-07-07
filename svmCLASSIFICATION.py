import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

kernel_gaussian = 0
kernel_linear = 1
kernel_polynomial = 0
def kernel(x,y):
	if kernel_gaussian:
		z = x-y
		gamma = 90 #gamma = 1/(2*sigma*sigma)
		K = np.exp(-gamma*np.power(LA.norm(z),2))
		return K
	elif kernel_linear:
		K=x*y
		return K.sum()
	elif kernel_polynomial:
		K=x*y
		order = 2
		k = np.power(K.sum(),order)
		return k


def findError(alpha,data,b,C,output):
	m,n=data.shape
	for i in range(m):
		y2 = data[i][n-1]
		point = data[i,0:n-1]
		error[i] = svm_output(data,alpha,point,b)-y2
		output[i] = np.sign(svm_output(data,alpha,point,b)*y2)
	return error 


def svm_output(data,alpha,point,b):
	m,n = data.shape
	out = 0
	for i in range(m):
		out += alpha[i]*data[i][n-1]*kernel(data[i,0:n-1],point)
	out += b[0]
	return out


def primal_object(alpha,data,b,C,output):
	out = 0
	m,n=data.shape
	for i in range(m):
		for j in range(m):
			y1 = data[i][n-1]
			y2 = data[j][n-1]
			point1 = data[i,0:n-1]
			point2 = data[j,0:n-1]
			out += alpha[i]*alpha[j]*y1*y2*kernel(point1,point2)
	E = np.zeros(m)
	for i in range(m):
		y2 = data[i][n-1]
		point = data[i,0:n-1]
		E[i] = max(0,1-svm_output(data,alpha,point,b)*y2)
	out = 0.5*out + C*(E.sum())
	return out

def dual_object(alpha,data):
	out = 0
	m,n=data.shape
	for i in range(m):
		for j in range(m):
			y1 = data[i][n-1]
			y2 = data[j][n-1]
			point1 = data[i,0:n-1]
			point2 = data[j,0:n-1]
			out += alpha[i]*alpha[j]*y1*y2*kernel(point1,point2)
	out = alpha.sum()-0.5*out
	return out




def takeStep(i1,i2,alpha,data,b,C,error,output):
	eps = 0.001
	if i1==i2:
		return 0
	alph1 = alpha[i1]
	alph2 = alpha[i2]
	y1 = data[i1][n-1]
	y2 = data[i2][n-1]
	point1 = data[i1,0:n-1]
	point2 = data[i2,0:n-1]
	error = findError(alpha,data,b,C,output)
	E1 = error[i1]
	E2 = error[i2]
	s = y1*y2
	if s==1:
		L = max(0, alph1+alph2-C)
		H = min(C, alph1+alph2)
	else:
		L = max(0, alph1-alph2)
		H = min(C, C-alph1+alph2)
	if L==H:
		return 0
	k11 = kernel(point1, point1)
	k12 = kernel(point1, point2)
	k22 = kernel(point2, point2)
	eta = 2*k12-k11-k22
	if eta < 0:
		a2 = alph2 - y2*(E1-E2)/eta
		if a2 < L:
			a2 = L
		elif a2 > H:
			a2 = H
	else:
		alpha1 = alpha
		alpha1[i2] = L
		Lobj = dual_object(alpha1,data)
		alpha1[i2]=H
		Hobj = dual_object(alpha1,data)
		if Lobj > Hobj+eps:
			a2 = L
		elif Lobj < Hobj-eps:
			a2 = H
		else:
			a2 = alph2
	if abs(a2-alph2) < eps*(a2+alph2+eps):
		return 0
	a1 = alph1 + s*(alph2-a2)
	alpha[i1]=a1
	alpha[i2]=a2

	print "updating threshold" 
	b1 = b[0]-E1-y1*(a1-alph1)*k11-y2*(a2-alph2)*k12
	b2 = b[0]-E2-y1*(a1-alph1)*k12-y2*(a2-alph2)*k22
	if b1==b2:
		b[0]=b1
	else:
		if a1 < C and a1 > 0:
			b[0] = b1
		elif a2 < C and a2 > 0:
			b[0] = b2
		else:
			b[0] = (b1+b2)/2
	print "threshhold updated"
	return 1

def second_hueristic(alpha,data,b,c,error,i2,output):
	m,n=data.shape
	error = findError(alpha,data,b,C,output)
	E2 = error[i2]
	maxi = None
	max_ind = None
	for i in range(m):
		if maxi is None:
			maxi = abs(error[i]-E2)
			max_ind = i
		else:
			if abs(error[i]-E2) > maxi:
				maxi = abs(error[i]-E2)
				max_ind = i
	return max_ind 
	

def check_example(i2,alpha,data,b,C,error,output,primal,dual):
	tol = 0.0001
	m,n = data.shape
	error = findError(alpha,data,b,C,output)
	alph2 = alpha[i2]
	y2 = data[i2][n-1]
	E2 = error[i2]
	r2 = E2*y2
	x = dual_object(alpha,data)
	y = primal_object(alpha,data,b,C,output)
	dual.append(x)
	primal.append(y)
	print x, y
	if (r2 < -tol and alph2 < C) or (r2 > tol and alph2 > 0):
		print "finding no of non-zero, non-C alphas"
		ind = np.where((alpha > 0) & (alpha < C))[0]
		indlist = ind.tolist()
		k = len(indlist)
		if k!=0:
			i1 = second_hueristic(alpha,data,b,C,error,i2,output)
			if takeStep(i1,i2,alpha,data,b,C,error,output):
				return 1
		
		if k!=0:
			for i1 in indlist:
				if takeStep(i1,i2,alpha,data,b,C,error,output):
					return 1
		
		for i1 in range(m):
			if i1!=i2:
				if takeStep(i1,i2,alpha,data,b,C,error,output):
					return 1
		print "finding completed"
	return 0

def plotdata(data):
	m,n = data.shape
	data1_x=[]
	data1_y=[]
	data2_x=[]
	data2_y=[]
	plt.figure(1)
	for i in range(m):
		if data[i][n-1]==1:
			data1_x.append(data[i][0])
			data1_y.append(data[i][1])
		elif data[i][n-1]==-1:
			data2_x.append(data[i][0])
			data2_y.append(data[i][1])
	plt.plot(data1_x,data1_y,'ro')
	plt.plot(data2_x,data2_y,'b*')
	plt.xlabel('------> x')
	plt.ylabel('------> y')
	plt.show()

if __name__ == '__main__':
	data = np.loadtxt("data1.csv",delimiter=",")
	(m,n)=data.shape
	plotdata(data)
	alpha = np.zeros(m)
	error = np.zeros(m)
	output = np.zeros(m)
	b = np.zeros(1)
	C = 0.5
	max_iter = 50
	num_iter=0
	num_changed = 0
	exam_all = 1
	primal = []
	dual = []
	while num_changed > 0 or exam_all:
		num_changed = 0

		if exam_all:
			for i in range(m):
				num_changed += check_example(i,alpha,data,b,C,error,output,primal,dual)
		else:
			for i in range(m):
				if alpha[i] > 0 and alpha[i] < C:
					num_changed += check_example(i,alpha,data,b,C,error,output,primal,dual)
		if exam_all == 1:
			exam_all = 0
		elif num_changed == 0:
			exam_all = 1
		print output
		ind = np.where(output==1)[0]
		num_iter += 1
		indlist = ind.tolist()
		k = len(indlist)
		print k
		l = 0.85*m
		if k > l or num_iter > max_iter:
			break

	for i in range(m):
		y2 = data[i][n-1]
		point = data[i,0:n-1]
		output[i] = np.sign(svm_output(data,alpha,point,b)*y2)
	
	print "threshold: ", b
	print "Alpha: ", alpha
	print "output: ", output
	plt.figure(2)
	for i in range(m):
		if alpha[i]==0:
			if data[i][n-1]==1:
				plt.plot(data[i][0],data[i][1],'ro')
			else:
				plt.plot(data[i][0],data[i][1],'r+')
		else:
			if data[i][n-1]==1:
				plt.plot(data[i][0],data[i][1],'bo')
			else:
				plt.plot(data[i][0],data[i][1],'b+')
	
	print "plotting decision boundary"
	xmin = min(data[:,0])
	xmax = max(data[:,0])
	ymin = min(data[:,1])
	ymax = max(data[:,1])
	print xmin, xmax, ymin, ymax
	boundary_x_0 = []
	boundary_y_0 = []
	boundary_x_1 = []
	boundary_y_1 = []
	boundary_x_2 = []
	boundary_y_2 = []
	for i in np.linspace(xmin-0.5, xmax+0.5, 200):
		for j in np.linspace (ymin-0.5, ymax+0.5, 200):
			point = np.array([i,j])
			out = svm_output(data,alpha,point,b)
			if out > -0.001 and out < 0.001:
				boundary_x_0.append(i)
				boundary_y_0.append(j)
			elif out > -1-0.001 and out < -1+0.001:
				boundary_x_1.append(i)
				boundary_y_1.append(j)
			elif out > 1-0.001 and out < 1+0.001:
				boundary_x_2.append(i)
				boundary_y_2.append(j)
	
	k = min(len(boundary_x_0),len(boundary_x_1),len(boundary_x_2))
	print k
	plt.plot(boundary_x_0[:],boundary_y_0[:],'b--') 
	plt.plot(boundary_x_1[:k],boundary_y_1[:k],'g--')
	plt.plot(boundary_x_2[:k],boundary_y_2[:k],'r--')
	plt.xlabel('-----------> x')
	plt.ylabel('-----------> y')
	plt.show()
	
	print "plot dual objective value vs iterations"
	k = min(len(primal), len(dual))
	plt.figure(3)
	plt.plot(range(k),primal[:k],'r-',label='Primal obj func')
	plt.plot(range(k),dual[:k],'b-',label='Dual obj func')
	plt.xlabel('------> iterations')
	plt.ylabel('------> objective function')
	plt.title('convergence plot')
	plt.axis([0,k,min(min(primal),min(dual)),max(max(primal),max(dual))])
	plt.show()
	
	
		

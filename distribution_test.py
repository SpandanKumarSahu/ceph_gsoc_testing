#!/usr/bin/python

def normalise( array ):
	return [float(i)/sum(array) for i in array]

def getWeights( checklist ):
	weight_list = []
	for i in checklist:
		weight_list.append(weights[i])
	return weight_list

def remove( checklist, i):
	checklist.remove(i)
	return checklist

def recfunc( replica_count, checklist, carry ):
	if (replica_count >= num_OSD):
		return
	norm_checklist = normalise( getWeights(checklist) )

	for i in range(num_OSD):
		if i in checklist:
			result_matrix[replica_count][i] += carry*(norm_checklist[checklist.index(i)])
			temp_checklist = list( checklist )
			temp_checklist.remove(i)
			recfunc(replica_count+1, temp_checklist, carry*norm_checklist[checklist.index(i)])
	
	
weights = list()
num_OSD = input("Enter number of OSDs: ")
result_matrix = []
norm_weights = []

for i in range(num_OSD):
	temp = []
	for j in range(num_OSD):
		temp.append(0)
	result_matrix.append(temp)

print "Enter the weight of the OSDs"
for i in range(num_OSD):
	temp = input()
	weights.append(temp)
norm_weights = normalise(weights)

for i in range(num_OSD):
	result_matrix[0][i] = norm_weights[i]

checklist = []
for i in range(num_OSD):
	checklist.append(i)

recfunc( 1, checklist, 1)

for i in range(1, num_OSD):
	result_matrix[i] = [x + y for x, y in zip(result_matrix[i-1], result_matrix[i])]

for i in range(num_OSD):
	result_matrix[i] = normalise(result_matrix[i])

for i in result_matrix:
	print i

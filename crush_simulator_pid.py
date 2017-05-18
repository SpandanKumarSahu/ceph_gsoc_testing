#!/usr/bin/python

# Assumptions : 
# 1. All objects are of same size
# 2. Ceph CRUSH behaves like random()

import os
import bisect as bisect
import random
import math

def normalise( array ):
	return [float(i)/sum(array) for i in array]

def remove( checklist, i):
	checklist.remove(i)
	return checklist

def reweight_after_replica_write():
	return	

def reweight_after_object_write():
	global current_load_distribution
	global norm_weights
	norm_current_load_distribution = normalise(current_load_distribution)
	global current_load_difference
	current_load_difference = [y - x for x, y in zip(norm_current_load_distribution, norm_weights)]
	global sum_load_difference
	sum_load_difference = [x + y for x, y in zip(current_load_difference, sum_load_difference)]
	global diff_load_difference
	diff_load_difference = [y - x for x, y in zip(norm_current_load_distribution, past_load_difference)]
	global past_load_difference
	past_load_difference = current_load_difference[:]	
	
	total_error = [ kp*x+ki*y+kd*z for x, y, z in zip(current_load_difference, sum_load_difference, diff_load_difference)]	
	total_error = [math.fabs(i) for i in total_error]
	norm_total_error = normalise(total_error)	

	global current_weights
	for i in range(num_OSD):
		current_weights[i] *= (1 + total_error[i] * norm_total_error[i])  

def getWeights( checklist ):
	weight_list = [current_weights[i] for i in checklist]
	return weight_list

def input_weights():
	print "Enter the weight of the OSDs: "
	for i in range(num_OSD):
		temp = input()
		weights.append(temp)
	norm_weights = normalise(weights)
	current_weights = norm_weights[:]	

def pick( checklist, random_number):
	temp_weights = normalise( getWeights(checklist) )
	for i in range(len(temp_weights)-1):
		temp_weights[i+1] += temp_weights[i]
	temp_weights[len(temp_weights)-1] = 1.0000000000000 
	index = bisect.bisect(temp_weights, random_number)
	current_load_distribution[checklist[index]] += 1
	del checklist[index]
	return checklist

weights = list()

num_OSD = input("Enter the number of OSDs: ")
replica_count = input("Enter the replica count (<num_OSD): ")
input_weights()
count_objects = 0

current_load_distribution = [0]*num_OSD
sum_load_difference = [0]*num_OSD
diff_load_difference = normalise(weights)
past_load_difference = [0]*num_OSD
kp = 0.8
ki = 0.1
kd = 0.00

current_weights = weights[:]
norm_weights = normalise(weights)

while (count_objects < 10000):
	checklist = range(num_OSD)
	picks = 0
	while (picks <= replica_count):
		checklist = pick(checklist, random.random())
		reweight_after_replica_write()
		picks += 1
	reweight_after_object_write()
	count_objects += 1	
	print normalise(current_load_distribution)


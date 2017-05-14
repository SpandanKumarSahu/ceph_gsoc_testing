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
	current_load_difference = [x - y for x, y in zip(normalise(current_load_distribution), norm_weights)]
	max_value = max(current_load_difference)
	min_value = min(current_load_difference)
	current_weights[current_load_difference.index(max_value)] *= math.pow(1-replica_count*0.01, replica_count)
	current_weights[current_load_difference.index(min_value)] *= math.pow(1+replica_count*0.01, replica_count)

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


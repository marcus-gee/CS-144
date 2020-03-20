#!/usr/bin/env python

import sys

#
# This program simply represents the reduce function.
#

first_node = True
output = 0
alpha = .85

for line in sys.stdin:
	line_formatted = line.split('\t')
	cur_node, pagerank_val = line_formatted[0], line_formatted[1]

	if cur_node == "ITERATION:":
		sys.stdout.write(line)

	else:
		# If this is the first node in the stream, set prev_node
		if first_node:
			prev_node = cur_node
			first_node = False

		# Check if we are in "input type 2"
		if "," in pagerank_val:
			# store this value
			neighbor_info = pagerank_val.split(",")

			# maybe bug check :)
			continue


		# If we are at the same node as the previous node in the stream
		# we continue summing our output
		if prev_node == cur_node:
		# CONTINUE SUMMING
			output += float(pagerank_val) * alpha

		else:
			# OUTPUT OUR VALUES
			output += (1 - alpha)
			output = str(output)
			sys.stdout.write(prev_node + "\t" + output + "\n")
			if type(neighbor_info) == str:
				neighbor_info = pagerank_val.split(",")


			neighbor_info[0] = output
			s = ","
			neighbor_info = s.join(neighbor_info)
			neigh_output = prev_node + "\t" + str(neighbor_info)


			sys.stdout.write(neigh_output) # + "\n")

			output = float(pagerank_val) * alpha
			prev_node = cur_node

			# RESET THE SUM


if prev_node != "ITERATION:":
	output += (1 - alpha)
	output = str(output)
	sys.stdout.write(prev_node + "\t" + output + "\n")

	neighbor_info[0] = output 
	s = ","
	neighbor_info = s.join(neighbor_info)
	neigh_output = prev_node + "\t" + str(neighbor_info)


	sys.stdout.write(neigh_output) # + "\n")







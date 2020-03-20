#!/usr/bin/env python

import sys

unsort_curr_ranks = []
unsort_prev_ranks = []
output_rankings = []
lines = []

max_iter = 10


for line in sys.stdin:
	line_formatted = line.split('\t')
	node, pagerank_val = line_formatted[0], line_formatted[1]

	if node == "ITERATION:":
		iteration = float(pagerank_val)
		if iteration < max_iter:
			iter_info = line

	else:
		if "," in pagerank_val:
			node_info = pagerank_val.split(',')
			curr_rank = node_info[0]
			prev_rank = node_info[1]
			unsort_curr_ranks.append((node, curr_rank, pagerank_val))
			unsort_prev_ranks.append((node, prev_rank))



# Sort by rank
sorted_curr_ranks = sorted(unsort_curr_ranks, key=lambda x: x[1], reverse = True)
sorted_prev_ranks = sorted(unsort_prev_ranks, key=lambda x: x[1], reverse = True)

lst_curr_nodes = [x[0] for x in sorted_curr_ranks]
lst_prev_nodes = [x[0] for x in sorted_prev_ranks]


if lst_curr_nodes[:20] == lst_prev_nodes[:20] or iteration >= max_iter:
	for i in range (20):
		string = "FinalRank:"
		pagerank = sorted_curr_ranks[i][1].strip()
		pagerank = str(pagerank)
		string += pagerank
		string += "\t"
		string += str(sorted_curr_ranks[i][0])
		string += "\n"
		sys.stdout.write(string)
	

else:
	for n in unsort_curr_ranks:
		sys.stdout.write("NodeId:" + str(n[0]) + '\t' + str(n[2]))
	sys.stdout.write(iter_info)
	

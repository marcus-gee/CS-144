#!/usr/bin/env python

import sys

#
# This program simply represents the map function.
#

iteration = 1

for line in sys.stdin:
    # parse data
    node_number, node_info = line.split('\t')
    ignore, node_id = node_number.split(':')
    
    if ignore == "ITERATION":
        iteration = str(int(node_info)+1)
        sys.stdout.write("ITERATION:\t" + iteration)

    else:
        info = node_info.strip().split(',')
        
        # split info into the rank_data and neighbor list
        rank_info, out_links = info[:2], info[2:]
        rank_info = [float(i) for i in rank_info]
        
        # update old rank
        rank_info[1] = rank_info[0]
        curr_rank = rank_info[0]
        
        # contribute its rank to itself if no out links
        if not out_links:
            
            sys.stdout.write(node_id + '\t' + str(curr_rank) + '\n')
        
        # ouput rank shared to out links
        else:
            for link in out_links:
                out_rank = curr_rank / float(len(out_links))
                if out_rank > 1e-3:
                    sys.stdout.write(link + '\t' + str(out_rank) + '\n')
        
        rank_info = [str(i) for i in rank_info]
        new_info = rank_info + out_links

        s = ","
        new_info = s.join(new_info)
        updated_info = node_id + '\t' + new_info + '\n'
        
        
        sys.stdout.write(updated_info)
        
if iteration == 1:
    sys.stdout.write("ITERATION:\t" + str(iteration))


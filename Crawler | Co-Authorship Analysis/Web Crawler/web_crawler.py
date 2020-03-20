import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from queue import Queue
from scipy.special import comb
from fetcher3 import *


'''
The function below contains the code to run the program which uses BFS to 
crawl the caltech.edu domain.

The crawler uses a Breadth First Search selection policy. The BFS allows
for a more a general look at the graph. This is because the BFS crawl we 
explore various parts of the graph by looking at nodes that go into many 
different areas of the caltech.edu domain, as opposed to searching the graph 
through one longer pathway. Further, I removed all nodes that were not in the 
caltech.edu domain (i.e. did not have caltech.edu in the URL). Also, I removed
any nodes with dynamic content (i.e. contained "?" in the URL). One 
disadvantage of the BFS method is that the max. diameter may be hard to 
calculate as we do not explore very deep into any one node pathway.
'''
def web_crawler(start_node, pages_to_crawl):
    
    # init all data structures
    q = Queue()
    G1 = nx.Graph()
    
    visited        = []
    links_from     = {}
    links_to       = {}
    
    
    # get first node
    q.put(start_node)
    
    # start BFS
    while q != [] and pages_to_crawl > 1:
        while True:
            # pop node
            curr_node = q.get()
    
            # clean URL
            if curr_node[-1] == '/': 
                curr_node = curr_node[:-1]
            if '?' not in curr_node and 'caltech.edu' in curr_node: 
                break
        
        # if hasn't been visited, mark as visited and fetch links
        if curr_node not in visited:
            visited.append(curr_node)
            links = fetch_links(curr_node)
            
            if links == None:
                links = []
                
            for link in links:
                
                # get all valid caltech.edu links
                if 'caltech.edu' in link:
                    if link[-1] == '/': 
                        link = link[:-1]
                
                    q.put(link)
                    G1.add_edge(curr_node, link)
                    
                    # list of all out degree neighbors
                    if curr_node in links_from:
                        links_from[curr_node].append(link)
                    else:
                        links_from[curr_node] = [link]
                        
                    # list of all in degree neighbors
                    if link in links_to:
                        links_to[link].append(curr_node)
                    else:
                        links_to[link] = [curr_node]
                            
        pages_to_crawl -= 1
    return (links_to, links_from)

    
    
if __name__ == "__main__":
    start_node = 'http://www.caltech.edu/'
    pages_to_crawl = 2000
    
    (links_to, links_from) = web_crawler(start_node, pages_to_crawl)
    
    
    # VISUALIZATIONS
    
    # HISTOGRAMS 
    # Out Degrees
    out_degrees = [len(links_from[k]) for k in list(links_from.keys())]
    fig, ax = plt.subplots()
    plt.hist(out_degrees, bins= 'auto', color='g', edgecolor='black', 
             linewidth=0.2)
    plt.xlabel('Degree')
    plt.ylabel('Count of Nodes')
    plt.title('Links Per Page (Out-Degree)');
    plt.savefig('links_from_histogram')
    plt.close()
    
    # In Degrees
    in_degrees = [len(links_to[k]) for k in list(links_to.keys())]
    fig, ax = plt.subplots()
    plt.hist(in_degrees, bins= 85, color='g', edgecolor='g')
    plt.xlabel('Degree')
    plt.ylabel('Count of Nodes')
    plt.title('Links To Each Page (In-Degree)');
    plt.savefig('links_to_histogram')
    plt.close()

    # CCDF's
    # Out Degrees
    cumulative_counts_out = np.cumsum(np.bincount(out_degrees))
    node_count_out = len(out_degrees)
    normalized_counts_out = [(node_count_out - x) / 
                             node_count_out for x in cumulative_counts_out]
    fig, ax = plt.subplots()
    plt.plot(normalized_counts_out, color= 'g')
    plt.xlabel('Degrees')
    plt.ylabel('Probability')
    plt.title('CCDF of Links Per Page')
    plt.savefig('links_from_ccdf')
    plt.close()
    
    # In Degrees
    cumulative_counts_in = np.cumsum(np.bincount(in_degrees))
    node_count_in = len(in_degrees)
    fig, ax = plt.subplots()
    normalized_counts_in = [(node_count_in - x) / 
                            node_count_in for x in cumulative_counts_in]
    plt.plot(normalized_counts_in, color= 'g')
    plt.xlabel('Degrees')
    plt.ylabel('Probability')
    plt.title('CCDF of Links To Each Page')
    plt.savefig('links_to_ccdf')  
    plt.close()
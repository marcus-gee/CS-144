import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import comb

def analyze_coauthorship(co_author_data):
    # read data containing all undirected edge pairs from txt file
    data = pd.read_csv(co_author_data, sep = " ", names = ['Author 1', 'Author 2'])
    
    # initialize graph
    G2 = nx.Graph()
    
    # populate graph with all edges from nodes
    for ind in data.index:
        G2.add_edge(data['Author 1'][ind], data['Author 2'][ind])
    
    # create table containing count of degress for each node 
    node_degree_data = pd.DataFrame(G2.degree(G2.nodes), columns = ['Node', 'Degree'])
    
    return node_degree_data


if __name__ == "__main__":
    node_data = analyze_coauthorship('gr_qc_coauthorships.txt')
    degrees = node_data['Degree'].tolist()
    
    # VISUALIZATIONS    
    # HISTOGRAM
    fig, ax = plt.subplots()
    plt.hist(degrees, bins= 'auto', color='g', edgecolor='black', linewidth=0.2)
    plt.xlabel('Degree')
    plt.ylabel('Count of Nodes')
    plt.title('Histogram of Node Degrees');
    plt.savefig('node_degree_histogram')
    plt.clf()
    
    # CCDF
    cumulative_counts = np.cumsum(np.bincount(degrees))
    node_count = len(degrees)
    normalized_counts = [(node_count - x) / node_count for x in cumulative_counts]
    plt.plot(normalized_counts, color= 'g')
    plt.xlabel('Degree')
    plt.ylabel('Probability')
    plt.title('CCDF of Node Degrees')
    plt.savefig('node_degree_ccdf')
    
    
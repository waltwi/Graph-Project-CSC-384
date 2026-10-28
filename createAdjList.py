import networkx as nx;
import pandas as pd;
import igraph as ig;

df = pd.read_csv('Graph Project CSC 384/git_web_ml/musae_git_edges.csv')

G = nx.from_pandas_edgelist(df, source = 'id_1', target = 'id_2')

adjacency_list = nx.to_dict_of_lists(G)


#If you would like to save the list as a file uncomment this section out!
#with open("adjacency_list.txt", "w", encoding="utf-8") as file:
    #for node, neighbors in adjacency_list.items():
        #file.write(f"{node}: {neighbors}\n")

#print(f"Saved adjacency lists for {len(adjacency_list)} nodes.")

nodes = list(dict.fromkeys(
    list(adjacency_list) + [v for neighbors in adjacency_list.values() for v in neighbors]
 ))
node_id = {node: i for i, node in enumerate(nodes)}

edges = {
    tuple(sorted((node_id[u], node_id[v])))
    for u, neighbors in adjacency_list.items()
    for v in neighbors
    if u != v
}

graph = ig.Graph(n = len(nodes), edges = list(edges), directed = False)

partition = graph.community_leiden(
    objective_function = 'modularity',
    resolution = 1.0,
    n_iterations=-1,
)

communities = [
    [nodes[i] for i in group]
    for group in partition
]

#uncomment this section if you would like to save the communities as a file!
#with open("communities.txt", "w", encoding="utf-8") as f:
    #for community_number, community in enumerate(communities, start=1):
        #members = ", ".join(str(node) for node in community)
        #f.write(f"Community {community_number}: {members}\n")

print(communities)
print("Modularity:", graph.modularity(partition.membership))


#uncomment this section if you would like to save the diagnostics as a file!
community_sizes = sorted(partition.sizes(), reverse=True)
component_sizes = sorted(
    graph.connected_components(mode="weak").sizes(),
    reverse=True,
)

with open("communities_diagnostics.txt", "w", encoding="utf-8") as f:
    f.write(f"Nodes: {graph.vcount()}\n")
    f.write(f"Edges: {graph.ecount()}\n")
    f.write(f"Communities: {len(community_sizes)}\n")
    f.write(f"Connected components: {len(component_sizes)}\n")
    f.write(f"Isolated nodes: {sum(d == 0 for d in graph.degree())}\n")

    top_ten_share = sum(community_sizes[:10]) / graph.vcount()
    f.write(f"Nodes in 10 largest communities: {top_ten_share:.2%}\n")

    f.write("\nCommunity sizes, largest first:\n")
    for rank, size in enumerate(community_sizes, start=1):
        f.write(
            f"{rank}: {size} nodes ({size / graph.vcount():.2%})\n"
        )

    f.write("\nConnected component sizes, largest first:\n")
    for rank, size in enumerate(component_sizes, start=1):
        f.write(f"{rank}: {size} nodes\n")
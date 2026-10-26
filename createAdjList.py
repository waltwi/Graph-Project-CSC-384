import networkx as nx;
import pandas as pd;

df = pd.read_csv('Graph Project CSC 384/git_web_ml/musae_git_edges.csv')

G = nx.from_pandas_edgelist(df, source = 'id_1', target = 'id_2')

adjacency_list = nx.to_dict_of_lists(G)

with open("adjacency_list.txt", "w", encoding="utf-8") as file:
    for node, neighbors in adjacency_list.items():
        file.write(f"{node}: {neighbors}\n")

print(f"Saved adjacency lists for {len(adjacency_list)} nodes.")
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
#from networkx.drawing.nx_agraph import graphviz_layout
#import pygraphviz


# GRAFO COMUM
#g = nx.Graph()
#g.add_node(1)
#
# g = nx.path_graph(4)
# pos = nx.kamada_kawai_layout(g)
# print(pos)

# DIGRAFO
g2 = nx.DiGraph()
g2.add_nodes_from([1,2,3,4])
g2.add_edges_from([(1,2), (1,3), (3,4)])

# g2.add_node(5)
# g2.add_edge(3,5)

g3 = nx.DiGraph()
g3.add_nodes_from(range(15,1,15))
g3.add_edges_from([(1,2), (2,9), (9,14), (1,3), (1,4),
                   (3,5), (5,10), (10,12), (12,13), (13,14),
                   (3,7), (3,8), (8,13), (7,11), (11,12), (3,6), (6,12),
                   (4,8), (14,1)])

# g3.add_edges_from([(1,2), (2,9),         (1,3), (1,4),
#                    (3,5), (5,10),         (12,13),
#                    (3,7), (3,8),         (7,11),          (3,6), (6,12),
#                    (13, 14)])

#edges = nx.draw_networkx_edges(g3, pos=nx.spring_layout(g3))

# pos = {1: np.array([-1, 0]), 2:np.array([-0.6, 0.5]),
#        3: np.array([-0.6, -0.5]), 4: np.array([-0.1, -0.7]), 5:([0,0])}
pos = {1: np.array([0,0.5]), 2: np.array([0.5, 1]), 3: np.array([0.5, 0]),
      4: np.array([1, 0.5])}

#pos = graphviz_layout(g3, prog='dot', args="-Grankdir=LR")

# pos = {1: np.array([0,0.5]), 2: np.array([0.25, 0.75]), 3: np.array([0.50, 0.75]),
#        4: np.array([0.75, 0.75]), 5: np.array([1,0.5])}

layer = 6
height = 5

pos = {1: np.array([0,0.5]),
       2: np.array([1/layer, 4/height]), 3:np.array([1/layer,2.5/height]), 4:np.array([1/layer,1/height]),
       9:np.array([2/layer,5/height]), 5:np.array([2/layer,3/height]), 6:np.array([2/layer,2.5/height]), 7:np.array([2/layer, 2/height]),
       10:np.array([3/layer,3/height]), 11:np.array([3/layer,2/height]), 8:np.array([3/layer,1/height]),
       12:np.array([4/layer,2.5/height]),
       13:np.array([5/layer, 2.5/height]),
       14:np.array([1, 1])}

# LAYOUT
#pos = nx.kamada_kawai_layout(g3)
# pos = nx.planar_layout(g3)
#pos = nx.bipartite_layout(g2)
#pos = nx.circular_layout(g2)
#pos = nx.fruchterman_reingold_layout(g2)
#pos = nx.shell_layout(g3)
#pos = nx.spectral_layout(g2, center=([0,0]))

ct = g3.copy()
ct.remove_edges_from([(9,14),(10,12),(11,12), (4,8), (8,13)])
nx.draw_networkx(g3, pos, with_labels=True)

#nx.draw
# Draw desatualizado
#nx.draw(g3, pos, with_labels=False)
plt.show()


# ADICIONANDO ATRIBUTO EM NÓ

#nome_grafo.nodes[nr_no][nome_atributo] = valor

# for node in g3.nodes:
#     print(type(node))

g3.succ


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

global CA, SS, DC, total_Rec, total_HS, total_compute, total_shift

def HS_main():
    print('HS')
    global CA, SS, DC, pos, total_HS
    total_HS += 1
    # print('total_HS: ', total_HS)
    CA = set()
    SS = set()
    SA, DC = Recursion(1)
    if SS != set():
        Shift_activities(SS)
        HS_main()
    else:
        DC_FINAL = 0.00

        for node in range(1, ct.number_of_nodes()+1):
            DC_FINAL += ct.nodes[node]['CF'] / ((1 + 0.01) ** (ct.nodes[node]['EARLY_START'] + ct.nodes[node]['DURATION']))
        print("The optimal solution is %d" % DC_FINAL)

        for node in range(1, ct.number_of_nodes()+1):
            print('Node: ', node, ' Early finish: ', ct.nodes[node]['EARLY_START'] + ct.nodes[node]['DURATION'])

        nx.draw_networkx(ct, pos, with_labels=True)
        #nx.draw_networkx_labels(graph, pos=pos, labels={data['CF']: data['CF'] for data in graph.nodes.values()})

        plt.show()

def Recursion(node):
    global CA
    global total_Rec
    global SS
    total_Rec += 1
    # print('total_Rec: ', total_Rec)

    SA = {node}
    DC = ct.nodes[node]['CF'] / ((1 + 0.01) ** (ct.nodes[node]['EARLY_START'] + ct.nodes[node]['DURATION']))
    CA.add(node)
    print('node: ', node)
    for i in list(ct.successors(node)):
        if i not in CA:
            SA_l, DC_l = Recursion(i)
            if DC_l >= 0:
                SA = SA.union(sorted(SA_l))
                DC += DC_l
            else:
                ct.remove_edge(node, i)
                SS.add(tuple(sorted(SA_l)))

    for j in ct.predecessors(node):
        if j not in CA:
            SA_l, DC_l = Recursion(j)
            SA = SA.union(sorted(SA_l))
            DC += DC_l

    return SA, DC


def Shift_activities(SS):
    global total_shift
    # total_shift += 1
    Z = []
    for SA in SS:
        for i in SA:
            Z.append(i)

    print('SS:', SS)
    while Z != []:
        total_shift += 1
        k, l, V_k_l = Compute_V_k_l(Z)
        for SA_l in SS:
            if k in SA_l:
                break
        for i in SA_l:
            es = ct.nodes[i]['EARLY_START']
            ct.nodes[i]['EARLY_START'] += V_k_l
            Z.remove(i)
        ct.add_edge(k, l)

def Compute_V_k_l(Z):
    global total_compute
    #total_compute += 1
    # print('Compute: ', total_compute)
    l = None
    V_k_l = None
    for k in Z:
        for suc in graph.successors(k):
            #total_compute += 1
            #if (suc not in Z):
            for i in Z:
                total_compute += 1
                if suc == i:
                    continue
                if (l is None) or \
                        ((graph.nodes[suc]['EARLY_START'] - graph.nodes[k]['EARLY_START']) <
                         (graph.nodes[l]['EARLY_START'] - graph.nodes[k]['EARLY_START'])):
                    if k == graph.number_of_nodes():
                        V_k_l = ct.nodes[suc]['EARLY_START'] - ct.nodes[k]['EARLY_START'] - (-delta_n)
                    else:
                        V_k_l = ct.nodes[suc]['EARLY_START'] - ct.nodes[k]['EARLY_START'] - ct.nodes[k]['DURATION']
    l = suc
    print('total_compute: ', total_compute)
    return k, l, V_k_l



#Original Project
delta_n = 44
total_HS = 0
total_Rec = 0
total_shift = 0
total_compute = 0


#SS = set()

#List of due (current tree)
ct_duration  = [0      ,   6,      5,  3,   1,   6,     2,   1,   4,   3,   2,        3,      5,           0]
#List of early start (current tree)
ct_es   = [0      ,   0,      0,  0,   5,   5,     5,   7,   6,   6,   7,       11,     14,     19]
# #List of early finish (current tree)
# ct_ef   = [0      ,   6,      5,  3,   6,  11,     7,   8,  10,   9,   9,       14,     19,     19]
#List of cash flow not discounted (current tree)
ct_cfn  = [0      ,-140,    318,312,-329, 153,   193, 361,  24,  33, 387,     -386,    171,           0]
# #List of predecessors (current tree)
# ct_pred = [[14]   , [1],    [1],[1], [3], [3],   [3], [7], [2], [5], [7],      [6],   [12],          []]
# #List of successors (current tree)
# ct_suc  = [[2,3,4], [9],[5,6,7], [],[10],[12],[8,11],  [],  [],  [],  [],     [13],     [],         [1]]
# #List of predecessors (original graph)
# gp_pred = [[]     , [1],    [1],[1], [3], [3],   [3], [4,7], [2], [5], [7],[6,10,11], [8,12],      [9,13]]
# #List of successors (original graph)
# gp_suc  = [[2,3,4], [9],[5,6,7],[8],[10],[12],[8,11],[13],[14],[12],[12],     [13],   [14],         []]


graph = nx.DiGraph()
graph.add_nodes_from(range(15,1,15))
graph.add_edges_from([(1,2), (2,9), (9,14), (1,3), (1,4),
                   (3,5), (5,10), (10,12), (12,13), (13,14),
                   (3,7), (3,8), (8,13), (7,11), (11,12), (3,6), (6,12),
                   (4,8), (14,1)])
layer = 6
height = 5
pos = {1: np.array([0,0.5]),
       2: np.array([1/layer, 4/height]), 3:np.array([1/layer,2.5/height]), 4:np.array([1/layer,1/height]),
       9:np.array([2/layer,5/height]), 5:np.array([2/layer,3/height]), 6:np.array([2/layer,2.5/height]), 7:np.array([2/layer, 2/height]),
       10:np.array([3/layer,3/height]), 11:np.array([3/layer,2/height]), 8:np.array([3/layer,1/height]),
       12:np.array([4/layer,2.5/height]),
       13:np.array([5/layer, 2.5/height]),
       14:np.array([1, 1])}

for node in range(1, graph.number_of_nodes() + 1):
    graph.nodes[node]['CF'] = ct_cfn[node - 1]
    graph.nodes[node]['DURATION'] = ct_duration[node - 1]
    graph.nodes[node]['EARLY_START'] = ct_es[node - 1]
    #graph.nodes[node]['EARLY_FINISH'] = ct_ef[node - 1]

ct = graph.copy()
ct.remove_edges_from([(9,14),(10,12),(11,12), (4,8), (8,13), (14,1)])

# for node in range(1,15):
#     print('Node: ', node, ct.nodes[node]['EARLY_START'], 'Duration: ',
#           ct.nodes[node]['DURATION'], ' ct_ef : ', ct_ef[node-1], 'CF: ', ct.nodes[node]['CF'], ' cfn: ', ct_cfn[node-1])

HS_main()
print('total_HS: ', total_HS)
print('total_Rec: ', total_Rec)
print('total_Shift: ', total_shift)
print('total_Compute ', total_compute)
#print('SS: ', SS)


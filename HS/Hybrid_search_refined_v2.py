import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from Early_tree_graph_refined import forward_pass, main
import time

global CA, SS, DC, total_Rec, total_HS, total_compute, total_shift


def HS_main():
    print('HS')
    global CA, SS, DC, pos, total_HS, DC_FINAL
    total_HS += 1
    # print('total_HS: ', total_HS)
    CA = set()
    SS = []
    SA, DC = Recursion(1)
    if SS != []:
        Shift_activities(SS)
        HS_main()
    else:
        DC_FINAL = 0.00

        for node in range(1, ct.number_of_nodes() + 1):
            DC_FINAL += ct.nodes[node]['CF'] / ((1 + 0.01) ** (ct.nodes[node]['EF']))
        print("The optimal solution is %d" % DC_FINAL)

        for node in range(1, ct.number_of_nodes() + 1):
            print('Node: ', node, ' Early finish: ', ct.nodes[node]['EF'])

        # nx.draw_networkx(ct, pos, with_labels=True)
        # #nx.draw_networkx_labels(graph, pos=pos, labels={data['CF']: data['CF'] for data in graph.nodes.values()})
        #
        # plt.show()


def Recursion(node):
    global CA
    global total_Rec
    global SS
    total_Rec += 1
    # print('total_Rec: ', total_Rec)

    SA = {'nodes': {node},
          'node_k': node,
          'node_l': ct.nodes[node]['NODE_MIN_CONSTRAINT'],
          'node_l_in_SS': False}
    DC = ct.nodes[node]['CF'] / ((1 + 0.01) ** (ct.nodes[node]['EF']))
    CA.add(node)
    print('node: ', node)
    for i in list(ct.successors(node)):
        if i not in CA:
            SA_l, DC_l = Recursion(i)

            if DC_l >= 0:
                # New function 'update_SA_constraint' is O(n)
                # SA, SA_l = update_SA_constraint(SA, SA_l)
                SA['nodes'] = SA['nodes'].union(sorted(SA_l['nodes']))
                DC += DC_l
            else:
                ct.remove_edge(node, i)
                SA_l = Compute_k_l_sub_tree(SA_l)
                SS.append(SA_l)
                print('SS: ', SS)

    for j in ct.predecessors(node):
        if j not in CA:
            SA_l, DC_l = Recursion(j)
            # SA, SA_l = update_SA_constraint(SA, SA_l)
            SA['nodes'] = SA['nodes'].union(sorted(SA_l['nodes']))
            DC += DC_l

    node_list = []
    for nodes_SS in SS:
        node_list.extend(nodes_SS['nodes'])
    for SA_l in SS:
        if (SA_l['node_l'] in node_list):
            SA_l['node_l_in_SS'] = True

    return SA, DC


def Compute_k_l_sub_tree(SA_l):
    global total_compute
    for node in SA_l['nodes']:
        min_distance = ct.deadline
        for suc in graph.successors(node):
            suc_inside_SA_l = False
            for j in SA_l['nodes']:
                total_compute += 1
                if suc == j:
                    suc_inside_SA_l = True
                    break
            if (suc_inside_SA_l == False) and \
                    (ct.nodes[suc]['EF'] - ct.nodes[node]['EF']) < min_distance:
                min_distance = ct.nodes[suc]['EF'] - ct.nodes[node]['EF']
                l = suc
                k = node

    SA_l['node_k'] = k
    SA_l['node_l'] = l
    return SA_l


# def update_SA_constraint(SA, SA_l):
#     global total_Rec
#     total_Rec += 1
#     if SA['node_l'] in SA_l['nodes']:
#         SA['node_l'] = SA_l['node_l']
#         SA['node_k'] = SA_l['node_k']
#     # elif (ct.nodes[SA_l['node_l']]['EF'] - ct.nodes[SA_l['node_l']]['DURATION']) < \
#     #         (ct.nodes[SA['node_l']]['EF'] - ct.nodes[SA['node_l']]['DURATION']):
#     elif ct.nodes[SA_l['node_l']]['EF'] < ct.nodes[SA['node_l']]['EF']:
#         SA['node_l'] = SA_l['node_l']
#         SA['node_k'] = SA_l['node_k']
#     return SA, SA_l

def Shift_activities(SS):
    global total_shift
    while SS != []:
        SA_current = Min_SA(SS)
        ES_l = (ct.nodes[SA_current['node_l']]['EF'] - ct.nodes[SA_current['node_l']]['DURATION'])
        ES_k = (ct.nodes[SA_current['node_k']]['EF'] - ct.nodes[SA_current['node_k']]['DURATION'])
        DURATION_K = ct.nodes[SA_current['node_k']]['DURATION']
        if SA_current['node_l'] == 1:
            step_size = ES_l - ES_k - (-ct.deadline)
        else:
            step_size = ES_l - ES_k - DURATION_K
            # step_size = ES_l - ES_k
        for node in SA_current['nodes']:
            total_shift += 1

            ct.nodes[node]['EF'] += step_size
        ct.add_edge(SA_current['node_k'], SA_current['node_l'])
        SA_current['node_l_in_SS'] = False
        SS.remove(SA_current)


def Min_SA(SS):
    global total_compute
    min_distance = ct.deadline

    for SA_current in SS:
        total_compute += 1
        # ES_l = (ct.nodes[SA_current['node_l']]['EF'] - ct.nodes[SA_current['node_l']]['DURATION'])
        # ES_k = (ct.nodes[SA_current['node_k']]['EF'] - ct.nodes[SA_current['node_k']]['DURATION'])
        ES_l = (ct.nodes[SA_current['node_l']]['EF'])
        ES_k = (ct.nodes[SA_current['node_k']]['EF'])

        # min_SA = SA_current
        if (ES_l - ES_k) < (min_distance):
            min_distance = ES_l - ES_k
            min_SA = SA_current

    return (min_SA)


total_HS = 0
total_Rec = 0
total_shift = 0
total_compute = 0

layer = 6
height = 5
pos = {1: np.array([0, 0.5]),
       2: np.array([1 / layer, 4 / height]), 3: np.array([1 / layer, 2.5 / height]),
       4: np.array([1 / layer, 1 / height]),
       9: np.array([2 / layer, 5 / height]), 5: np.array([2 / layer, 3 / height]),
       6: np.array([2 / layer, 2.5 / height]), 7: np.array([2 / layer, 2 / height]),
       10: np.array([3 / layer, 3 / height]), 11: np.array([3 / layer, 2 / height]),
       8: np.array([3 / layer, 1 / height]),
       12: np.array([4 / layer, 2.5 / height]),
       13: np.array([5 / layer, 2.5 / height]),
       14: np.array([1, 1])}

layer = 7
height = 3
pos = {1: np.array([0, 0.5]),
       2: np.array([1 / layer, 3 / height]), 3: np.array([1.3 / layer, 2 / height]),
       4: np.array([1 / layer, 1 / height]),
       5: np.array([2 / layer, 3 / height]), 6: np.array([2.3 / layer, 2 / height]),
       7: np.array([2 / layer, 1 / height]),
       8: np.array([3 / layer, 3 / height]), 9: np.array([3.3 / layer, 2 / height]),
       10: np.array([3 / layer, 1 / height]),
       11: np.array([4 / layer, 3 / height]), 12: np.array([4.3 / layer, 2 / height]),
       13: np.array([4 / layer, 1 / height]),
       14: np.array([5 / layer, 3 / height]), 15: np.array([5.3 / layer, 2 / height]),
       16: np.array([5 / layer, 1 / height]),
       17: np.array([1, 1])}

ct, graph = main()

t1 = time.time()
HS_main()
t2 = time.time()
print(t2 - t1)
print('total_HS: ', total_HS)
print('total_Rec: ', total_Rec)
print('total_Shift: ', total_shift)
print('total_Compute ', total_compute)

print('total geral', total_HS + total_Rec + total_shift + total_compute)

nx.draw_networkx(ct, pos, with_labels=True)
# nx.draw_networkx(ct, nx.circular_layout(ct), with_labels=True)

plt.title('Scheduled - HS Refined_v2 \n' 'File name: ' + ct.file_name)
# plt.text(-0.2, 0.05, 'Duration:')
# plt.text(-0.2, 0, [ct.nodes[node]['DURATION'] for node in ct.nodes], size=9)
# plt.text(-0.2, -0.05, 'Cash flow:')
# plt.text(-0.2, -0.1, [ct.nodes[node]['CF'] for node in ct.nodes], size=9)
# plt.text(-0.2, -0.15, 'Early finish:')
# plt.text(-0.2, -0.2, [ct.nodes[node]['EF'] for node in ct.nodes], size=9)
# plt.text(-0.2, -0.25, 'Node min constraint:')
# plt.text(-0.2, -0.3, [ct.nodes[node]['NODE_MIN_CONSTRAINT'] for node in ct.nodes], size=9)
# plt.text(-0.2, -0.37, 'NPV:')
# plt.text(-0.1, -0.45, DC_FINAL)

plt.text(-0.2, 0.2, 'Duration:')
plt.text(-0.2, 0.15, [ct.nodes[node]['DURATION'] for node in ct.nodes], size=9)
plt.text(-0.2, 0.10, 'Cash flow:')
plt.text(-0.2, 0.05, [ct.nodes[node]['CF'] for node in ct.nodes], size=8)
plt.text(-0.2, 0.00, 'Early finish:')
plt.text(-0.2, -0.05, [ct.nodes[node]['EF'] for node in ct.nodes], size=9)
plt.text(-0.2, -0.10, 'Node min constraint:')
plt.text(-0.2, -0.15, [ct.nodes[node]['NODE_MIN_CONSTRAINT'] for node in ct.nodes], size=9)
plt.show()

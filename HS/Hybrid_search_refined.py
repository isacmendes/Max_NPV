from Early_tree_graph_refined import main as early_tree_main
from PluginGraph.Plotter import *
import time

global CA, SS, DC, total_Rec, total_HS, total_compute, total_shift

def Hybrid_search():
    # print('HS')
    global CA, SS, DC, pos, total_HS, DC_FINAL
    total_HS += 1
    CA = set()
    SS = []
    Recursion(1)

    if SS != []:
        Shift_activities(SS)
        Hybrid_search()
    else:
        DC_FINAL = 0.00

        for node in range(1, ct.number_of_nodes() + 1):
            DC_FINAL += ct.nodes[node]['CF'] / ((1 + 0.01) ** (ct.nodes[node]['EF']))
        print("The optimal solution is %d" % DC_FINAL)

        #plt_17("Original HS", DC_FINAL, ct)
        plt_main_example("Original HS", DC_FINAL, ct)


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
                SA, SA_l = update_SA_constraint(SA, SA_l)
                SA['nodes'] = SA['nodes'].union(sorted(SA_l['nodes']))
                DC += DC_l
            else:
                ct.remove_edge(node, i)
                SS.append(SA_l)
                print('SS: ', SS)

    for j in ct.predecessors(node):
        if j not in CA:

            SA_l, DC_l = Recursion(j)
            SA, SA_l = update_SA_constraint(SA, SA_l)
            SA['nodes'] = SA['nodes'].union(sorted(SA_l['nodes']))
            DC += DC_l

    node_list = []
    for nodes_SS in SS:
        node_list.extend(nodes_SS['nodes'])
    for SA_l in SS:
        if (SA_l['node_l'] in node_list):
            SA_l['node_l_in_SS'] = True

    return SA, DC

def update_SA_constraint(SA, SA_l):
    global total_Rec
    total_Rec += 1
    if SA['node_l'] in SA_l['nodes']:
        SA['node_l'] = SA_l['node_l']
        SA['node_k'] = SA_l['node_k']
    # elif (ct.nodes[SA_l['node_l']]['EF'] - ct.nodes[SA_l['node_l']]['DURATION']) < \
    #         (ct.nodes[SA['node_l']]['EF'] - ct.nodes[SA['node_l']]['DURATION']):
    elif ct.nodes[SA_l['node_l']]['EF'] < ct.nodes[SA['node_l']]['EF']:
        SA['node_l'] = SA_l['node_l']
        SA['node_k'] = SA_l['node_k']
    return SA, SA_l

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
            #step_size = ES_l - ES_k
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
        #ES_l = (ct.nodes[SA_current['node_l']]['EF'] - ct.nodes[SA_current['node_l']]['DURATION'])
        #ES_k = (ct.nodes[SA_current['node_k']]['EF'] - ct.nodes[SA_current['node_k']]['DURATION'])
        ES_l = (ct.nodes[SA_current['node_l']]['EF'])
        ES_k = (ct.nodes[SA_current['node_k']]['EF'])

        min_SA = SA_current
        if (SA_current['node_l_in_SS'] == True):
            if (ES_l - ES_k) < (min_distance):
                min_distance = ES_l - ES_k
                min_SA = SA_current

    return(min_SA)

total_HS = 0
total_Rec = 0
total_shift = 0
total_compute = 0

ct, graph = early_tree_main("HS v1")

Hybrid_search()

print('total_HS: ', total_HS)
#print('total_Rec: ', total_Rec)
print('total_Shift: ', total_shift)
print('total_Compute ', total_compute)

print('total geral', total_HS + total_shift + total_compute)

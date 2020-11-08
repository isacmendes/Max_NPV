# -*- coding: utf-8 -*-
from Early_tree_graph_refined import main as early_tree_main
from PluginGraph.Plotter import *


def Hybrid_search():
    global ct, graph, CA, SS, call_HS
    call_HS += 1

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
        #print("The optimal solution is %d" % DC_FINAL)

        # plt_17("Original HS", DC_FINAL, ct)
        #plt_general("Original HS", DC_FINAL, ct)
        # plt_main_example("Original HS", DC_FINAL, ct)


def Recursion(node):
    global SS, ct, call_Rec
    call_Rec += 1
    SA = {node}
    DC = ct.nodes[node]['CF'] / ((1 + 0.01) ** (ct.nodes[node]['EF']))
    CA.add(node)

    for i in list(ct.successors(node)):
        if i not in CA:
            SA_l, DC_l = Recursion(i)
            if DC_l >= 0:
                SA = SA.union(sorted(SA_l))
                DC += DC_l
            else:
                ct.remove_edge(node, i)
                SS.append(SA_l)

    for j in list(ct.predecessors(node)):
        if j not in CA:
            SA_l, DC_l = Recursion(j)
            SA = SA.union(sorted(SA_l))
            DC += DC_l

    return SA, DC


def Shift_activities(SS_l):
    global call_Shift, it_Shift

    call_Shift += 1
    Z = []
    for SA in SS_l:
        for i in SA:
            Z.append(i)

    while Z != []:
        k, l, V_k_l = Compute_V_k_l(Z)
        for SA_l in SS_l:
            if k in SA_l:
                break
        for i in SA_l:
            it_Shift += 1
            ct.nodes[i]['EF'] += V_k_l
            Z.remove(i)
        ct.add_edge(k, l)


def Compute_V_k_l(Z):
    global call_Compute, it_Compute

    call_Compute += 1
    # l = None
    V_k_l = 0
    Z_dem = []
    # min_distance = int(ct.deadline)

    for SA_l in Z:
        if isinstance(SA_l, list):
            for node in SA_l:
                Z_dem.append(node)
        else:
            Z_dem.append(SA_l)
    min_distance = ct.deadline
    for pred in Z_dem:
        for suc in graph.successors(pred):
            it_Compute += 1
            if suc not in Z_dem:
                s_k = ct.nodes[pred]['EF'] - ct.nodes[pred]['DURATION']
                d_k = ct.nodes[pred]['DURATION']
                s_l = ct.nodes[suc]['EF'] - ct.nodes[suc]['DURATION']
                if (s_l - ct.nodes[pred]['EF']) < min_distance:
                    min_distance = s_l - ct.nodes[pred]['EF']
                    if pred == graph.number_of_nodes():
                        V_k_l = s_l - s_k - (-ct.deadline)
                        l = 1
                    else:
                        V_k_l = s_l - s_k - d_k
                        l = suc
                    k = pred

    return k, l, V_k_l


#    except Exception:
#        print("Problems with file: ", graph.name)


def main(current_tree, original_graph):
    global ct, graph, call_HS, call_Rec, call_Compute, it_Compute, call_Shift, it_Shift

    # ct, graph = early_tree_main("HS")
    ct = current_tree
    graph = original_graph
    call_HS, call_Rec, call_Shift, it_Shift, call_Compute, it_Compute = 0, 0, 0, 0, 0, 0
    # plt_general("Original HS", 0, current_tree)

    Hybrid_search()

    # print("-----------\nCONTADORES:\n-----------")
    # print("Chamadas recursivas Hybrid_search(): ", total_HS)
    # print("Chamadas recursivas Recursion(): ", total_Rec)
    # print("Iterações Shift_activities(): ", total_shift)
    # print("Iterações Compute_V_K_l(): ", total_compute)
    # print('Total geral', total_HS + total_shift + total_compute)

    iterations = it_Shift + it_Compute
    #iterations = it_Compute
    #recursion_calls = call_HS + call_Rec
    recursion_calls = call_Rec

    # print('-' * 30)
    # print('HS')
    # print('total_main: ', total_HS)
    # print('total_Rec: ', total_Rec)
    # print('total_compute: ', total_compute)
    # print('-' * 30)
    # print('id ct: ', id(ct))
    return iterations, \
           recursion_calls, \
           call_HS, \
           call_Rec, \
           call_Shift, \
           it_Shift, \
           call_Compute, \
           it_Compute, \
           graph.number_of_nodes(), \
           graph.number_of_edges()


#call_HS, call_Rec, call_Shift, it_Shift, call_Compute, it_Compute = 0, 0, 0, 0, 0, 0

# main()

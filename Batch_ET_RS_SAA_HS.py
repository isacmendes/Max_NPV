# Title     : Batch ET, RS, SAA and HS
# Objective : Counting iterations and recusive calls
# Created by: Isac
# Created on: 17/10/2020

from ImportGraph import import_graph
from Early_tree_graph_refined import forward_pass
from RS.Recursive_search_original import main as RS_main
from SAA.SAA_original import main as SAA_main
from HS.Hybrid_search_original import main as HS_main
import time
import sys
sys.setrecursionlimit(25000)

# import igraph as ig

def Batch_ET_RS_SAA_HS():
    #TESTE...
    #pkg_graph = import_graph('Samples/Lotes_2a_Rodada/Lote_1')
    pkg_graph = import_graph('Samples')
    pkg_et_RS = {}
    pkg_et_SAA = {}
    pkg_et_HS = {}

    # Totais RS:
    total_itera_RS = 0
    total_calls_RS = 0
    total_Step_3_RS = 0
    total_Rec_RS = 0
    total_shift_it_RS = 0
    total_nodes_RS = 0
    total_Compute_call_RS = 0
    total_Compute_it_RS = 0
    total_edges_RS = 0

    # Totais SAA:
    total_itera_SAA = 0
    total_calls_SAA = 0
    total_SAD_it_SAA = 0
    total_SAD_call_SAA = 0
    total_VA_EDGES_it_SAA = 0
    total_VA_shifts_it_SAA = 0
    total_VA_call_SAA = 0
    total_Compute_it_SAA = 0
    total_Compute_call_SAA = 0
    total_nodes_SAA = 0
    total_edges_SAA = 0

    # Totais HS:
    total_itera_HS = 0
    total_calls_HS = 0
    total_HS_call = 0
    total_Rec_call_HS = 0
    total_Shift_call_HS = 0
    total_Shift_it_HS = 0
    total_Compute_call_HS = 0
    total_Compute_it_HS = 0
    total_nodes_HS = 0
    total_edges_HS = 0

    # Variables for count min and max nodes and edges
    min_nodes, max_nodes = 100000, 0
    min_nodes_file, max_nodes_file = None, None
    min_edges, max_edges = 100000, 0
    min_edges_file, max_edges_file = None, None

    count = 0
    for i, current_file_graph in enumerate(pkg_graph.items()):
        count += 1
        current_file_name, original_graph = current_file_graph[0], current_file_graph[1]

        print('File: ', current_file_name)

        # Count min and max nodes and edges
        if min_nodes >= original_graph.number_of_nodes():
            min_nodes = original_graph.number_of_nodes()
            min_nodes_file = original_graph.name

        if max_nodes <= original_graph.number_of_nodes():
            max_nodes = original_graph.number_of_nodes()
            max_nodes_file = original_graph.name

        if min_edges >= original_graph.number_of_edges():
            min_edges = original_graph.number_of_edges()
            min_edges_file = original_graph.name

        if max_edges <= original_graph.number_of_edges():
            max_edges = original_graph.number_of_edges()
            max_edges_file = original_graph.name

        # Call SAA:
        et_SAA = forward_pass(original_graph, "SAA", current_file_name)
        pkg_et_SAA[i] = et_SAA
        current_itera_SAA, \
        current_calls_SAA, \
        SAD_it_SAA, \
        SAD_call_SAA, \
        VA_EDGES_it_SAA, \
        VA_shifts_it_SAA, \
        VA_call_SAA, \
        Compute_it_SAA, \
        Compute_call_SAA, \
        nodes_SAA, \
        edges_SAA, = SAA_main(et_SAA, original_graph)

        total_itera_SAA += current_itera_SAA
        total_calls_SAA += current_calls_SAA
        total_SAD_it_SAA += SAD_it_SAA
        total_SAD_call_SAA += SAD_call_SAA
        total_VA_EDGES_it_SAA += VA_EDGES_it_SAA
        total_VA_shifts_it_SAA += VA_shifts_it_SAA
        total_VA_call_SAA += VA_call_SAA
        total_Compute_it_SAA += Compute_it_SAA
        total_Compute_call_SAA += Compute_call_SAA
        total_nodes_SAA += nodes_SAA
        total_edges_SAA += edges_SAA

        # Call HS
        et_HS = forward_pass(original_graph, "HS", current_file_name)
        current_itera_HS, \
        current_calls_HS, \
        HS_call, \
        Rec_call_HS, \
        Shift_call_HS, \
        Shift_it_HS, \
        Compute_call_HS, \
        Compute_it_HS, \
        nodes_HS, \
        edges_HS= HS_main(et_HS, original_graph)

        total_itera_HS += current_itera_HS
        total_calls_HS += current_calls_HS
        total_HS_call += HS_call
        total_Rec_call_HS += Rec_call_HS
        total_Shift_call_HS += Shift_call_HS
        total_Shift_it_HS += Shift_it_HS
        total_Compute_call_HS += Compute_call_HS
        total_Compute_it_HS += Compute_it_HS
        total_nodes_HS += nodes_HS
        total_edges_HS += edges_HS

        #Call RS
        et_RS = forward_pass(original_graph, "RS", current_file_name)
        pkg_et_RS[i] = et_RS

        current_itera_RS, \
        current_calls_RS, \
        Step_3_RS, \
        Rec_RS, \
        Shift_it_RS, \
        Compute_it_RS, \
        Compute_call_RS, \
        nodes_RS, \
        edges_RS, ctRS = RS_main(et_RS, original_graph)

        total_itera_RS += current_itera_RS
        total_calls_RS += current_calls_RS
        total_Step_3_RS += Step_3_RS
        total_Rec_RS += Rec_RS
        total_shift_it_RS += Shift_it_RS
        total_Compute_call_RS += Compute_call_RS
        total_Compute_it_RS += Compute_it_RS
        total_nodes_RS += nodes_RS
        total_edges_RS += edges_RS

    print('count: ', count)
    # General statistic with MIN and MAX (nodes and edges)
    print("General statistics:")
    print('-' * 35)
    print("File name with MIN NODES: ", min_nodes_file)
    print("MIN Number of nodes in this file is: ", min_nodes)
    print("File name with MAX NODES: ", max_nodes_file)
    print("MAX Number of nodes in this file is: ", max_nodes)

    print("File name with MIN EDGES: ", min_edges_file)
    print("MIN Number of edges in this file is: ", min_edges)
    print("File name with MAX EDGES: ", max_edges_file)
    print("MAX Number of edges in this file is: ", max_edges)

    # Summary SAA
    print("\n")
    print("-" * 35)
    print("RESUME - Steepest Ascent Approach:".upper())
    print("Iterations average: ", total_itera_SAA / len(pkg_graph))
    print("Recursive function calls average: ", total_calls_SAA / len(pkg_graph))
    print("Considered projects: ", len(pkg_graph))
    print("TOTAL AVERAGE SAA: ", (total_itera_SAA + total_calls_SAA) / len(pkg_graph))
    print("-" * 35)
    print("DETAIL SAA: ")
    print("SAD_it_SAA AVG: ", total_SAD_it_SAA / len(pkg_graph))
    print("SAD_call_SAA: AVG ", total_SAD_call_SAA / len(pkg_graph))
    print("VA_EDGES_it_SAA: ", total_VA_EDGES_it_SAA / len(pkg_graph))
    print("VA_shifts_it_SAA: ", total_VA_shifts_it_SAA / len(pkg_graph))
    print("VA_call_SAA: ", total_VA_call_SAA / len(pkg_graph))
    print("Compute_it_SAA: ", total_Compute_it_SAA / len(pkg_graph))
    print("Nodes SAA AVG: ", total_nodes_SAA / len(pkg_graph))
    print("Edges SAA AVG: ", total_edges_SAA / len(pkg_graph))
    print("-" * 35)

    # Summary HS
    print("\n")
    print("-" * 35)
    print("RESUME - Hybrid Search:".upper())
    print("Iterations average: ", total_itera_HS / len(pkg_graph))
    print("Recursive function calls average: ", total_calls_HS / len(pkg_graph))
    print("Considered projects: ", len(pkg_graph))
    print("TOTAL AVERAGE HS: ", (total_itera_HS + total_calls_HS) / len(pkg_graph))
    print("-" * 35)
    print("DETAIL HS: ")
    print("HS_call AVG: ", total_HS_call / len(pkg_graph))
    print("Rec_call_HS AVG: ", total_Rec_call_HS / len(pkg_graph))
    print("Shift_call_HS: ", total_Shift_call_HS / len(pkg_graph))
    print("Shift_it_HS: ", total_Shift_it_HS / len(pkg_graph))
    print("Compute_call_HS: ", total_Compute_call_HS / len(pkg_graph))
    print("Compute_it_HS: ", total_Compute_it_HS / len(pkg_graph))
    print("Nodes HS AVG: ", total_nodes_HS / len(pkg_graph))
    print("Edges HS AVG: ", total_edges_HS / len(pkg_graph))
    print("-" * 35)

    # Summary RS
    print("\n")
    print("-" * 35)
    print("RESUME - Recursive Search:".upper())
    print("Iterations average: ", (total_itera_RS / len(pkg_graph)))
    print("Recursive function calls average: ", total_calls_RS / len(pkg_graph))
    print("Considered projects: ", len(pkg_graph))
    print("TOTAL AVERAGE RS: ", (total_itera_RS + total_calls_RS) / len(pkg_graph))

    print("-" * 35)
    print("DETAIL RS: ")
    print("Step_3_RS AVG: ", total_Step_3_RS / len(pkg_graph))
    print("Rec_RS: AVG ", total_Rec_RS / len(pkg_graph))
    print("Shift_it_RS: ", total_shift_it_RS / len(pkg_graph))
    print("Compute_call_RS AVG: ", total_Compute_call_RS / len(pkg_graph))
    print("Compute_it_RS AVG: ", total_Compute_it_RS / len(pkg_graph))
    print("Nodes RS AVG: ", total_nodes_RS / len(pkg_graph))
    print("Edges RS AVG: ", total_edges_RS / len(pkg_graph))
    print("-" * 35)


t1 = time.time()
Batch_ET_RS_SAA_HS()
t2 = time.time()

print("Execution time: ", t2 - t1)

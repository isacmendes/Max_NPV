# Hybrid Search

# global CA
# global DC_final
# global SS
# global total_Rec
# global total_HRS

def Hybrid_recursive_search():
    global CA
    global SS
    global total_HRS
    global DC

    total_HRS += 1

    CA = set()
    SS = []
    Rec(1)
    print('CA: ', CA)
    if SS != []:
        Shift_activities(SS)
        print('Considered Activities (CA): ', CA)
    else:
        print('The final Discounted Cash Flow is:... ')

def Rec(no):
    global total_Rec
    global degree_acumulated
    global SS

    total_Rec += 1
    DC_final = False
    SA = [no]
    DC = ct_cfn[no - 1] / ((1 + 0.01) ** ct_ef[no - 1])  # Discounted Cash flow
    CA.add(no - 1)
    print('Nó visitado %d' %(no))
    for j in sorted(ct_suc[no - 1]):
        if j - 1 not in CA:
            SA_l, DC_l = Rec(j)
            if DC_l >= 0:
                SA.extend(SA_l)
                DC += DC_l
            else:
                if DC_final != True:
                    print("Remove conection between i: ", no, " and j: ", j)
                    ct_suc[no - 1].remove(j)  # Remove successor from CT
                    ct_pred[j - 1].remove(no)  # Remove predecessor from CT

                    # Insert vertex in an orderly way, taking into account the calculated degree
                    for item in SA_l:
                        start = 0
                        end = len(SS)
                        binary_insertion(item, start, end)

    for j in ct_pred[no - 1]:
        if j - 1 not in CA:
            SA_l, DC_l = Rec(j)  # SA_l and DC_l are SA and DC of node successor in the back recursion
            SA.extend(SA_l)
            DC += DC_l

    actual_SA = set(SA)

    if len(original_set.difference(actual_SA)) == 0:
        DC_final = True

    return SA, DC

def binary_insertion(item, start, end):
    global count_binary_insertion
    count_binary_insertion += 1
    if len(SS) == 0:
        SS.append(item)
    else:
        middle = (start + end) // 2
        if start >= end:
            if end <= 0:
                if degree_acumulated[item - 1] > degree_acumulated[SS[0] - 1]:
                    SS.insert(1, item)
                else:
                    SS.insert(0, item)
            elif start >= len(SS):
                if degree_acumulated[item - 1] > degree_acumulated[SS[-1] - 1]:
                    SS.append(item)
                else:
                    SS.insert(len(SS), item)
            else:
                if degree_acumulated[item - 1] > degree_acumulated[SS[middle - 1] - 1]:
                    SS.insert(middle + 1, item)
                else:
                    SS.insert(middle, item)

        elif degree_acumulated[item - 1] == degree_acumulated[SS[middle] - 1]:
            SS.insert(middle, item)
        elif (degree_acumulated[item - 1] > degree_acumulated[SS[middle] - 1]):
            start = middle + 1
            binary_insertion(item, start, end)
        elif (degree_acumulated[item - 1] < degree_acumulated[SS[middle] - 1]):
            end = middle - 1
            binary_insertion(item, start, end)



def Rec_Degree(no, last_degree=0):
    global total_rec_degree
    global gp_suc
    global degree_acumulated
    global dummy_final
    global count_visited

    if no == 14:
        dummy_final += 1
        print('Número de visitas ao Dummy final: ', dummy_final)
    total_rec_degree += 1
    print('Nó visitado %d' %(no))
    degree_acumulated[no - 1] += last_degree + 1
    print(degree_acumulated)
    for j in sorted(gp_suc[no - 1]):
        if j != 14:
            Rec_Degree(j, degree_acumulated[no - 1])


    count_visited[no - 1] += 1

def Shift_activities(SS):
    pass


#####################
#       Main        #
#####################
"""
global DC_FINAL
global total_Rec
global total_Step3
"""
DC_final = False
delta_n = 44  # Deadline of project
total_Rec = 0
total_Step3 = 0
CA_UpdateEft = set()
total_rec_degree = 1
CA = set()
count_visited = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#count_visited = [0,0,0,0,0,0,0,0]
# count_visited = [0,0,0,0,0,0]
count_binary_insertion = 0

dummy_final = 0
SS = []

# New example
# List of due (current tree)
ct_due = [0, 1, 1, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1, 0] #OK
# List of early start (current tree)
ct_es = [0, 0, 1, 2, 3, 4, 7, 1, 0, 3, 4, 5, 5, delta_n] #OK
# List of early finish (current tree)
ct_ef = [0, 1, 2, 3, 4, 6, 2, 1, 3, 4, 5, 5, 2, delta_n]
# List of cash flow not discounted (current tree)
ct_cfn = [0, -10, 1, 1, 1, 1, 1, 1, -10, 1, 1, 1, 1, 0]
# List of predecessors (current tree)
ct_pred = [[], [1], [1], [1], [3], [3], [3], [7], [2], [5], [7], [6], [12], []]
# List of successors (current tree updated for new example)
ct_suc = [[2, 8], [3,7], [4], [5], [6], [14], [], [9], [10], [11,12], [], [14], [14], []]

# List of predecessors (original graph)
gp_pred = [[], [1], [1], [1], [3], [3], [3], [7], [2], [5], [7], [6, 10, 11], [8, 12], [9, 13]]
# List of successors (original graph)
#         Dummy1   A2     B3    C4      D5      E6     F7    G8   H9    I10       J11   K12   L13  Dummy2
gp_suc = [[2, 8], [3,7],  [4],  [5],    [6],    [14],  [9],  [9], [10], [11,12],  [6], [14], [14], []]
gp_pred = [[]   ,  [1] ,  [2],  [3],    [4],    [5] ,  [2],  [1], [8] , [9]    , [10], [10], [8] , [6, 12]]
ct_cfn = [0     ,  -10 ,    1,    1,      1,       1,    1,    1,  -10,       1,    1,    1,    1,       0]
ct_suc = [[2, 8], [3,7],  [4],  [5],    [6],      [],   [],  [9], [10], [11,12],   [],   [],   [], []]
ct_pred = [   [],   [1],  [2],  [3],    [4],     [5],  [2],  [1],  [8],     [9], [10], [10],  [8], []]
# #TESTE 1
# gp_suc = [[2, 8], [3,7], [4,9], [5,10], [6,11], [14,12], [9], [9], [10], [11,12], [6], [14], [14], []]

# #TESTE 2  Dummy1   A2     B3    C4      D5      E6     F7    G8      H9       I10     J11      K12   L13  Dummy2
# gp_suc = [[2, 3], [3,4], [3,4], [5,6], [5,6], [7,8], [7,8], [9,10], [9,10], [11,12], [11,12], [14], [14], []]
#
# #TESTE 3  Dummy1   A2     B3    C4      D5     E6    F7     G8        H9       I10      J11     K12   L13  Dummy2
# gp_suc = [[2, 3], [4,5], [4,5], [6,7], [6,7], [8,9], [8,9], [10,11], [10,11], [12,13], [12,13], [14], [14], []]

# #TESTE 4  Dummy1      A2       B3       C4       D5        E6        F7         G8          H9         I10       J11   K12   L13  Dummy2
# gp_suc = [[2,3,4], [5,6,7], [5,6,7], [5,6,7], [8,9,10], [8,9,10], [8,9,10], [11,12,13], [11,12,13], [11,12,13], [14], [14], [14], []]


# #TESTE 3  Dummy1   A2     B3    C4      D5    E6    F7
# gp_suc = [[2, 3], [4,5], [4,5], [6,7], [6,7], [8], [8], []]

#
# #TESTE 5  Dummy1   A2     B3     C4       D5
# gp_suc = [[2, 3], [4,5], [4,5],  [6],     [6], []]


# List of degree of nodes (current tree)
degree_acumulated = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# # Original Project
# # List of due (current tree)
# ct_due = [0, 6, 5, 3, 1, 6, 2, 1, 4, 3, 2, 3, 5, 0]
# # List of early start (current tree)
# ct_es = [0, 0, 0, 0, 6, 6, 6, 8, 7, 7, 8, 12, 15, delta_n]
# # List of early finish (current tree)
# ct_ef = [0, 6, 5, 3, 6, 11, 7, 8, 10, 9, 9, 14, 19, delta_n]
# # List of cash flow not discounted (current tree)
# ct_cfn = [0, -140, 318, 312, -329, 153, 193, 361, 24, 33, 387, -386, 171, 0]
# # List of predecessors (current tree)
# ct_pred = [[], [1], [1], [1], [3], [3], [3], [7], [2], [5], [7], [6], [12], []]
# # List of successors (current tree)
# ct_suc = [[2, 3, 4], [9], [5, 6, 7], [], [10], [12], [8, 11], [], [], [], [], [13], [14], []]
# # List of predecessors (original graph)
# gp_pred = [[], [1], [1], [1], [3], [3], [3], [7], [2], [5], [7], [6, 10, 11], [8, 12], [9, 13]]
# # List of successors (original graph)
# gp_suc = [[2, 3, 4], [9], [5, 6, 7], [8], [10], [12], [8, 11], [13], [14], [12], [12], [13], [14], []]
# # List of degree of nodes (current tree)
# degree_acumulated = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


original_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

Rec_Degree(1,0)
print('count_visited: ', count_visited)
#Rec_Degree_double(1,0)
#Rec_Degree_forward(1,0)
# Rec_Degree_backward(14,0)
print('Total Rec_Degree: ', total_rec_degree)


Rec(1)
Shift_activities(SS)

# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()

# total_Rec = 0
# total_HRS = 0
#
# Hybrid_recursive_search()
# Hybrid_recursive_search()
#
# print("1) Original project with 14 nodes")
# print("Total of HRS: %d and total of Rec: %d" % (total_HRS, total_Rec))
# print(ct_ef, "\n")

# # Demonstration
# # 1) Project with 11 nodes (sequence and negative flows at the begin)
# ct_due = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_es = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, delta_n]
# ct_ef = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, delta_n]
# ct_cfn = [0, -9, -9, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_pred = [[11], [1], [2], [3], [4], [5], [6], [7], [8], [9], []]
# ct_suc = [[2], [3], [4], [5], [6], [7], [8], [9], [10], [], [1]]
# gp_pred = [[], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
# gp_suc = [[2], [3], [4], [5], [6], [7], [8], [9], [10], [11], []]
#
# original_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
# total_Rec = 0
# total_Step3 = 0
# Hybrid_recursive_search()
# #SA, DC = Step_3()
# print("1) Project with 11 nodes (sequence and negative flows at the begin)")
# print("Total of Step3: %d and total of Rec: %d" % (total_Step3, total_Rec))
# print(ct_ef, "\n")

# # 2) Project with 11 nodes (sequence and negative flows at the end)
# ct_due = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_es = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, delta_n]
# ct_ef = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, delta_n]
# ct_cfn = [0, 1, 1, 1, 1, 1, 1, -9, -9, 1, 0]
# ct_pred = [[11], [1], [2], [3], [4], [5], [6], [7], [8], [9], []]
# ct_suc = [[2], [3], [4], [5], [6], [7], [8], [9], [10], [], [1]]
# gp_pred = [[], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
# gp_suc = [[2], [3], [4], [5], [6], [7], [8], [9], [10], [11], []]
#
# original_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("2) Project with 11 nodes (sequence and negative flows at the end)")
# print("Total of Step3: %d and total of Rec: %d" % (total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# # 3) Project with 20 nodes (sequence and negative flows at the end)
# ct_due = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_es = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, delta_n]
# ct_ef = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, delta_n]
# ct_cfn = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2, -2, 1, 0]
# # ct_cfn  = [0   ,-2 , -2, -2, -2, -2, -2, -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,   1,       0] #2 until 8 negatives
# ct_pred = [[20], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], []]
# ct_suc = [[2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [], [1]]
# gp_pred = [[], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19]]
# gp_suc = [[2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], []]
#
# original_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("3) Project with 20 nodes (sequence and negative flows at the end)")
# print("Total of Step3: %d and total of Rec: %d" % (total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# # 4) Project with 11 nodes (with two ways)
# ct_due = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_es = [0, 0, 0, 1, 1, 2, 2, 3, 3, 4, delta_n]
# ct_ef = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, delta_n]
# ct_cfn = [0, 1, 1, 1, 1, 1, -9, -9, 1, 1, 0]
# ct_pred = [[11], [1], [1], [2], [3], [4], [5], [6], [7], [8], []]
# ct_suc = [[2, 3], [4], [5], [6], [7], [8], [9], [10], [], [], [1]]
# gp_pred = [[], [1], [1], [2], [3], [4], [5], [6], [7], [8], [9, 10]]
# gp_suc = [[2, 3], [4], [5], [6], [7], [8], [9], [10], [11], [11], [1]]
#
# original_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("4) Project with 11 nodes (with two ways)")
# print("Total of Step3: %d and total of Rec: %d" % (total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# # 5) Project with 11 nodes (with five ways)
# ct_due = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_es = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, delta_n]
# ct_ef = [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, delta_n]
# ct_cfn = [0, 1, 1, 1, -9, -9, 1, 1, 1, 1, 0]
# ct_pred = [[11], [1], [1], [1], [3], [3], [3], [5], [6], [7], []]
# ct_suc = [[2, 3, 4], [], [5, 6, 7], [], [8], [9], [10], [], [], [], [1]]
# gp_pred = [[], [1], [1], [1], [3], [3], [3], [5], [6], [7], [8, 9, 10]]
# gp_suc = [[2, 3, 4], [5], [5, 6, 7], [7], [8], [9], [10], [11], [11], [11], []]
#
# original_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("5) Project with 11 nodes (with five ways)")
# print("Total of Step3: %d and total of Rec: %d" % (total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# # 6) Project with 11 nodes (with six ways)
# ct_due = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_es = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, delta_n]
# ct_ef = [0, 1, 1, 1, 2, 2, 2, 2, 2, 2, delta_n]
# ct_cfn = [0, -9, -9, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_pred = [[11], [1], [1], [1], [2], [2], [3], [3], [4], [4], []]
# ct_suc = [[2, 3, 4], [5, 6], [7, 8], [9, 10], [], [], [], [], [], [], [1]]
# gp_pred = [[], [1], [1], [1], [2], [2], [3], [3], [4], [4], [5, 6, 7, 8, 9, 10]]
# gp_suc = [[2, 3, 4], [5, 6], [7, 8], [9, 10], [11], [11], [11], [11], [11], [11], [1]]
#
# original_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("6) Project with 11 nodes (with six ways)")
# print("Total of Step3: %d and total of Rec: %d" % (total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# print("\n\n NEW STANDARD")
# # 7) Project 11 with nodes, with three levels (three sons)
# ct_due = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_es = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, delta_n]
# ct_ef = [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, delta_n]
# ct_cfn = [0, -9, 1, -9, 1, 1, 1, 1, 1, 1, 0]
# ct_pred = [[11], [1], [1], [1], [3], [3], [3], [6], [6], [6], []]
# ct_suc = [[2, 3, 4], [], [5, 6, 7], [], [], [8, 9, 10], [], [], [], [], [1]]
# gp_pred = [[], [1], [1], [1], [2, 3], [3], [3, 4], [5, 6], [6], [6, 7], [8, 9, 10]]
# gp_suc = [[2, 3, 4], [5], [5, 6, 7], [7], [8], [8, 9, 10], [10], [11], [11], [11], []]
#
# original_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("7) Project with 11 nodes, with three levels (three sons)")
# print("Total of Step3: %d and total of Rec: %d" % (total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# # 8) Project with 14 nodes, with four levels (three sons)
# ct_due = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_es = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, delta_n]
# ct_ef = [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, delta_n]
# ct_cfn = [0, -20, 1, -20, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_pred = [[14], [1], [1], [1], [3], [3], [3], [6], [6], [6], [9], [9], [9], []]
# ct_suc = [[2, 3, 4], [], [5, 6, 7], [], [], [8, 9, 10], [], [], [11, 12, 13], [], [], [], [], [1]]
# gp_pred = [[], [1], [1], [1], [2, 3], [3], [3, 4], [5, 6], [6], [6, 7], [8, 9], [9], [9, 10], [11, 12, 13]]
# gp_suc = [[2, 3, 4], [5], [5, 6, 7], [7], [8], [8, 9, 10], [10], [11], [11, 12, 13], [13], [14], [14], [14], []]
#
# original_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("8) Project with 14 nodes, with four levels (three sons)")
# print("Total of Step3: %d and total of Rec: %d" % (total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# # 9) Project with 17 nodes, with five levels (three sons)
# ct_due = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_es = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, delta_n]
# ct_ef = [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, delta_n]
# ct_cfn = [0, -20, 1, -20, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_pred = [[17], [1], [1], [1], [3], [3], [3], [6], [6], [6], [9], [9], [9], [12], [12], [12], []]
# ct_suc = [[2, 3, 4], [], [5, 6, 7], [], [], [8, 9, 10], [], [], [11, 12, 13], [], [], [14, 15, 16], [], [], [], [], [1]]
# gp_pred = [[], [1], [1], [1], [2, 3], [3], [3, 4], [5, 6], [6], [6, 7], [8, 9], [9], [9, 10], [11, 12], [12], [12, 13],
#            [14, 15, 16]]
# gp_suc = [[2, 3, 4], [5], [5, 6, 7], [7], [8], [8, 9, 10], [10], [11], [11, 12, 13], [13], [14], [14, 15, 16], [16],
#           [17], [17], [17], []]
#
# original_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("9) Project with 17 nodes, with five levels (three sons)")
# print("Total of Step3: %d and total of Rec: %d" % (total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# # 10) Project with 20 nodes, with six levels (three sons)
# ct_due = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_es = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, delta_n]
# ct_ef = [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, delta_n]
# ct_cfn = [0, -20, 1, -20, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ct_pred = [[20], [1], [1], [1], [3], [3], [3], [6], [6], [6], [9], [9], [9], [12], [12], [12], [15], [15], [15], []]
# ct_suc = [[2, 3, 4], [], [5, 6, 7], [], [], [8, 9, 10], [], [], [11, 12, 13], [], [], [14, 15, 16], [], [],
#           [17, 18, 19], [], [], [], [], [1]]
# gp_pred = [[], [1], [1], [1], [2, 3], [3], [3, 4], [5, 6], [6], [6, 7], [8, 9], [9], [9, 10], [11, 12], [12], [12, 13],
#            [14, 15], [15], [15, 16], [17, 18, 19]]
# gp_suc = [[2, 3, 4], [5], [5, 6, 7], [7], [8], [8, 9, 10], [10], [11], [11, 12, 13], [13], [14], [14, 15, 16], [16],
#           [17], [17, 18, 19], [19], [20], [20], [20], []]
#
# original_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("10) Project with 20 nodes, with six levels (three sons)")
# print("Total of Step3: %d and total of Rec: %d" % (total_Step3, total_Rec))
# print(ct_ef, "\n")
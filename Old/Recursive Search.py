#Step 3

def Rec(no):
    #print("called Rec in Node: ", no)
    global CA
    global DC_FINAL
    global total_Rec
    total_Rec += 1
    DC_FINAL = False
    SA = [no]
    DC = ct_cfn[no-1]/((1+0.01) ** ct_ef[no-1])             #Discounted Cash flow
    CA.add(no-1)
    for j in ct_suc[no-1]:
        if j-1 not in CA:
            SA_l, DC_l = Rec(j)
            if DC_l >= 0:
                SA.extend(SA_l)
                SET_ACT = SA
                DC += DC_l
            else:
                if DC_FINAL != True:
                    print("Remove conection between i: ", no, " and j: ", j)
                    ct_suc[no-1].remove(j)                  #Remove successor from CT
                    ct_pred[j-1].remove(no)                 #Remove predecessor from CT

                    # Versão errada
                    #last_node = LastNode_SA_l(SA_l)         #Find last node of SA_l to conect it with the nearest successor node
                    #nn = FindNearest(last_node-1)           #Find the nearest node (nn) of last node of SA_l

                    # Versão corrigida
                    last_node, nn = New_LastNode_SA_l(SA_l)

                    # Refinamento 1
                    #last_node, nn = MinStep(SA_l)

                    if nn not in ct_suc[last_node-1]:
                        
                        ct_suc[last_node-1].append(nn)      #Connect the last SA node with the closest restriction (successor)
                        ct_pred[nn-1].append(last_node)     #Connect the last SA node with the closest restriction (predecessor)
                        print("Conectou ", last_node, " e ", nn)
                        print(ct_suc)
                    
                    CA_UpdateEft.clear()
                    if ct_ef[nn-1] == delta_n:
                        UpdateEft(SA_l, last_node, ct_es[nn-1]+1, 'suc')
                    else:
                        UpdateEft(SA_l, last_node, ct_es[nn-1], 'suc')
                    
                    Step_3()                                #After pruning and connecting to the nearest boundary, resets the scanning
                    
    tem_pred =  ct_pred[no-1]
    for j in ct_pred[no-1]:        
        if j-1 not in CA:
            SA_l, DC_l = Rec(j)                             #SA_l and DC_l are SA and DC of node successor in the back recursion
            SA.extend(SA_l)                                 
            DC += DC_l                                      

    actual_SA = set(SA)

    if len(original_set.difference(actual_SA)) == 0:
        DC_FINAL = True
        
    return  SA, DC
    
def Step_3():
    #print("Called Step_3")
    global CA
    global total_Step3
    total_Step3 += 1
    CA = set()
    SA,DC = Rec(1)        
    return SA,DC

def FindNearest(last_node_SA):
    suc_list = gp_suc[last_node_SA]
    early_suc = 0                                           #Assigment index 0 with early_suc util find another early_suc
    for i in suc_list[1:]:  
        if ct_es[suc_list[i-1]] < ct_es[suc_list[early_suc]-1]:
            early_suc = i
    return suc_list[early_suc]

def UpdateEft(SA_l, node, limit, origination):
    global CA_UpdateEft
    
    if origination == 'suc':
        ct_ef[node-1] = limit - 1
        ct_es[node-1] = ct_ef[node-1] - (ct_due[node-1]-1)
    else:
        ct_ef[node-1] = limit + 1
        ct_es[node-1] = ct_ef[node-1] - (ct_due[node-1]-1)
    CA_UpdateEft.add(node)
    
    for i in ct_suc[node-1]:
        if (i not in CA_UpdateEft) and (i in SA_l):
            UpdateEft(SA_l, i, ct_es[node-1], 'pred')
    
    for j in ct_pred[node-1]:
        if j not in CA_UpdateEft and (j in SA_l):
            UpdateEft(SA_l, j, ct_es[node-1], 'suc')

def LastNode_SA_l(list_SA_l):
    index_major_finish = list_SA_l[0]
    for i in list_SA_l[1:]:
        if ct_ef[index_major_finish-1] < ct_ef[i-1]:
            index_major_finish = i
    return index_major_finish

# Correção na primeira versão - O(m)
def New_LastNode_SA_l (list_SA_l):
    global NLN
    min_step_node = len(gp_suc)
    last_node = list_SA_l[0]
    for node_sa in list_SA_l:
        for node_suc in gp_suc[node_sa-1]:
            NLN += 1
            if node_suc not in list_SA_l:
                if ct_es[node_suc-1] <= ct_es[min_step_node-1]:
                    last_node = node_sa
                    min_step_node = node_suc

    return last_node, min_step_node

# Refinamento 2
def MinStep(list_SA_l):
    global MS
    min_step_node = len(gp_suc)
    #last_node = min_constraint[list_SA_l[0]]
    for node_sa in list_SA_l:
        MS += 1
        if min_constraint[node_sa-1] not in list_SA_l:
            last_node = node_sa
            min_step_node = min_constraint[node_sa-1]
    return last_node, min_step_node


#####################
#       Main        #
#####################
"""
global DC_FINAL
global total_Rec
global total_Step3
"""
DC_FINAL = False
delta_n = 44 #Deadline of project
total_Rec = 0
total_Step3 = 0
CA_UpdateEft = set()

MS = 0
NLN = 0

#Original Project
#List of due (current tree)
ct_due  = [0      ,   6,      5,  3,   1,   6,     2,   1,   4,   3,   2,        3,      5,           0]
#List of early start (current tree)
ct_es   = [0      ,   0,      0,  0,   6,   6,     6,   8,   7,   7,   8,       12,     15,     delta_n]
#List of early finish (current tree)
ct_ef   = [0      ,   6,      5,  3,   6,  11,     7,   8,  10,   9,   9,       14,     19,     delta_n]
#List of cash flow not discounted (current tree)
ct_cfn  = [0      ,-140,    318,312,-329, 153,   193, 361,  24,  33, 387,     -386,    171,           0]
#List of predecessors (current tree)
ct_pred = [[14]   , [1],    [1],[1], [3], [3],   [3], [7], [2], [5], [7],      [6],   [12],          []]
#List of successors (current tree)
ct_suc  = [[2,3,4], [9],[5,6,7], [],[10],[12],[8,11],  [],  [],  [],  [],     [13],     [],         [1]]
#List of predecessors (original graph)
gp_pred = [[]     , [1],    [1],[1], [3], [3],   [3], [4,7], [2], [5], [7],[6,10,11], [8,12],      [9,13]]
#List of successors (original graph)
gp_suc  = [[2,3,4], [9],[5,6,7],[8],[10],[12],[8,11],[13],[14],[12],[12],     [13],   [14],         []]

min_constraint = [-1, 9, 6, 8, 10, 12, 11, 13, 14, 12, 12, 13, 14, 1]

original_set = set([1,2,3,4,5,6,7,8,9,10,11,12,13,14])
total_Rec = 0
total_Step3 = 0
SA, DC = Step_3()
print("1) Original project with 14 nodes")
print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
print(ct_ef, "\n")

print("MS: ", MS, "NLN: ", NLN)

########### NEW EXAMPLE
# DC_FINAL = False
# delta_n = 30 #Deadline of project
# total_Rec = 0
# total_Step3 = 0
# CA_UpdateEft = set()
#
# #Original Project
# #List of due (current tree)
# ct_due  = [0      ,   1,      3,  1,   1,   1,     1,   1,   3,      1,      1,        1,      1,           0]
# #List of early start (current tree)
# ct_es   = [0      ,   0,      0,  1,   1,   2,     3,   3,   3,      4,      4,        5,      5,     delta_n]
# #List of early finish (current tree)
# ct_ef   = [0      ,   1,      3,  2,   2,   3,     4,   4,   6,      5,      5,        6,      6,     delta_n]
# #List of cash flow not discounted (current tree)
# ct_cfn  = [0      ,-100,     10, 10,  10,  10,  -100,  10,  10,     10,     10,       10,     10,           0]
# #List of predecessors (current tree)
# ct_pred = [[14]   , [1],    [1],[2], [2], [4],   [3], [3], [6],    [7],    [9],     [10],   [10],          []]
# #List of successors (current tree)
# ct_suc  = [[2,3], [4,5],  [7,8],[6],  [], [9],  [10],  [],[11],[12,13],     [],       [],     [],         [1]]
# #List of predecessors (original graph)
# gp_pred = [[]   , [1]  ,    [1],[2], [2], [4], [3,5], [3], [6],    [7], [9,12],     [10],   [10],     [11,13]]
# #List of successors (original graph)
# gp_suc  = [[2,3], [4,5],  [7,8],[6],  [7], [9], [10],[14],[11],[12,13],   [14],     [11],   [14],          []]
#
# original_set = set([1,2,3,4,5,6,7,8,9,10,11,12,13,14])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("1) New example project with 14 nodes")
# print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
# print(ct_ef, "\n")
###########

# #Demonstration
# #1) Project with 11 nodes (sequence and negative flows at the begin)
# ct_due  = [0   , 1 ,  1,  1,  1,  1,  1,  1,   1,   1,         0]
# ct_es   = [0   , 0 ,  1,  2,  3,  4,  5,  6,   7,   8,   delta_n]
# ct_ef   = [0   , 1 ,  2,  3,  4,  5,  6,  7,   8,   9,   delta_n]
# ct_cfn  = [0   ,-9 , -9,  1,  1,  1,  1,  1,   1,   1,         0]
# ct_pred = [[11],[1],[2],[3],[4],[5],[6],[7], [8], [9],        []]
# ct_suc  = [[2] ,[3],[4],[5],[6],[7],[8],[9],[10],  [],       [1]]
# gp_pred = [[]  ,[1],[2],[3],[4],[5],[6],[7], [8], [9],      [10]]
# gp_suc  = [[2] ,[3],[4],[5],[6],[7],[8],[9],[10],[11],        []]
#
# original_set = set([1,2,3,4,5,6,7,8,9,10,11])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("1) Project with 11 nodes (sequence and negative flows at the begin)")
# print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
# print(ct_ef, "\n")
#
#
# #2) Project with 11 nodes (sequence and negative flows at the end)
# ct_due  = [0   , 1 ,  1,  1,  1,  1,  1,  1,   1,   1,         0]
# ct_es   = [0   , 0 ,  1,  2,  3,  4,  5,  6,   7,   8,   delta_n]
# ct_ef   = [0   , 1 ,  2,  3,  4,  5,  6,  7,   8,   9,   delta_n]
# ct_cfn  = [0   , 1 ,  1,  1,  1,  1,  1, -9,  -9,   1,         0]
# ct_pred = [[11],[1],[2],[3],[4],[5],[6],[7], [8], [9],        []]
# ct_suc  = [[2] ,[3],[4],[5],[6],[7],[8],[9],[10],  [],       [1]]
# gp_pred = [[]  ,[1],[2],[3],[4],[5],[6],[7], [8], [9],      [10]]
# gp_suc  = [[2] ,[3],[4],[5],[6],[7],[8],[9],[10],[11],        []]
#
# original_set = set([1,2,3,4,5,6,7,8,9,10,11])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("2) Project with 11 nodes (sequence and negative flows at the end)")
# print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# #3) Project with 20 nodes (sequence and negative flows at the end)
# ct_due  = [0   , 1 ,  1,  1,  1,  1,  1,  1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,       0]
# ct_es   = [0   , 0 ,  1,  2,  3,  4,  5,  6,   7,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17, delta_n]
# ct_ef   = [0   , 1 ,  2,  3,  4,  5,  6,  7,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18, delta_n]
# ct_cfn  = [0   , 1 ,  1,  1,  1,  1,  1,  1,   1,   1,   1,   1,   1,   1,  -2,  -2,  -2,  -2,   1,       0]
# #ct_cfn  = [0   ,-2 , -2, -2, -2, -2, -2, -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,   1,       0] #2 until 8 negatives
# ct_pred = [[20],[1],[2],[3],[4],[5],[6],[7], [8], [9],[10],[11],[12],[13],[14],[15],[16],[17],[18],      []]
# ct_suc  = [[2] ,[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],  [],     [1]]
# gp_pred = [[]  ,[1],[2],[3],[4],[5],[6],[7], [8], [9],[10],[11],[12],[13],[14],[15],[16],[17],[18],    [19]]
# gp_suc  = [[2] ,[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],      []]
#
# original_set = set([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("3) Project with 20 nodes (sequence and negative flows at the end)")
# print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# #4) Project with 11 nodes (with two ways)
# ct_due  = [0      ,   1 ,      1,     1,   1,   1,   1,   1,   1,   1,             0]
# ct_es   = [0      ,   0 ,      0,     1,   1,   2,   2,   3,   3,   4,       delta_n]
# ct_ef   = [0      ,   1 ,      1,     2,   2,   3,   3,   4,   4,   5,       delta_n]
# ct_cfn  = [0      ,   1 ,      1,     1,   1,   1,  -9,  -9,   1,   1,             0]
# ct_pred = [[11]   ,  [1],    [1],   [2], [3], [4], [5], [6], [7], [8],            []]
# ct_suc  = [[2,3]  ,  [4],    [5],   [6], [7], [8], [9],[10],  [],  [],           [1]]
# gp_pred = [[]     ,  [1],    [1],   [2], [3], [4], [5], [6], [7], [8],        [9,10]]
# gp_suc  = [[2,3]  ,  [4],    [5],   [6], [7], [8], [9],[10],[11],[11],           [1]]
#
# original_set = set([1,2,3,4,5,6,7,8,9,10,11])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("4) Project with 11 nodes (with two ways)")
# print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# #5) Project with 11 nodes (with five ways)
# ct_due  = [0      ,   1 ,      1,     1,   1,   1,   1,   1,   1,   1,             0]
# ct_es   = [0      ,   0 ,      0,     0,   1,   1,   1,   2,   2,   2,       delta_n]
# ct_ef   = [0      ,   1 ,      1,     1,   2,   2,   2,   3,   3,   3,       delta_n]
# ct_cfn  = [0      ,   1 ,      1,     1,  -9,  -9,   1,   1,   1,   1,             0]
# ct_pred = [[11]   ,  [1],    [1],   [1], [3], [3], [3], [5], [6], [7],            []]
# ct_suc  = [[2,3,4],   [],[5,6,7],    [], [8], [9],[10],  [],  [],  [],           [1]]
# gp_pred = [[]     ,  [1],    [1],   [1], [3], [3], [3], [5], [6], [7],      [8,9,10]]
# gp_suc  = [[2,3,4],  [5],[5,6,7],   [7], [8], [9],[10],[11],[11],[11],            []]
#
# original_set = set([1,2,3,4,5,6,7,8,9,10,11])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("5) Project with 11 nodes (with five ways)")
# print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# #6) Project with 11 nodes (with six ways)
# ct_due  = [0      ,   1 ,    1,     1,   1,   1,   1,   1,   1,   1,             0]
# ct_es   = [0      ,   0 ,    0,     0,   1,   1,   1,   1,   1,   1,       delta_n]
# ct_ef   = [0      ,   1 ,    1,     1,   2,   2,   2,   2,   2,   2,       delta_n]
# ct_cfn  = [0      ,  -9 ,   -9,     1,   1,   1,   1,   1,   1,   1,             0]
# ct_pred = [[11]   ,  [1],  [1],   [1], [2], [2], [3], [3], [4], [4],            []]
# ct_suc  = [[2,3,4],[5,6],[7,8],[9,10],  [],  [],  [],  [],  [],  [],           [1]]
# gp_pred = [[]     ,  [1],  [1],   [1], [2], [2], [3], [3], [4], [4],[5,6,7,8,9,10]]
# gp_suc  = [[2,3,4],[5,6],[7,8],[9,10],[11],[11],[11],[11],[11],[11],           [1]]
#
# original_set = set([1,2,3,4,5,6,7,8,9,10,11])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("6) Project with 11 nodes (with six ways)")
# print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
# print(ct_ef, "\n")
#
#
# print("\n\n NEW STANDARD")
# #7) Project 11 with nodes, with three levels (three sons)
# ct_due  = [0       , 1 ,      1,  1,    1,       1,    1,    1,   1,     1,             0]
# ct_es   = [0       , 0 ,      0,  0,    1,       1,    1,    2,   2,     2,       delta_n]
# ct_ef   = [0       , 1 ,      1,  1,    2,       2,    2,    3,   3,     3,       delta_n]
# ct_cfn  = [0       ,-9 ,      1, -9,    1,       1,    1,    1,   1,     1,             0]
# ct_pred = [[11]    ,[1],    [1],[1],  [3],     [3],  [3],  [6], [6],   [6],            []]
# ct_suc  = [[2,3,4] , [],[5,6,7], [],   [],[8,9,10],   [],   [],  [],    [],           [1]]
# gp_pred = [[]      ,[1],    [1],[1],[2,3],     [3],[3,4],[5,6], [6], [6,7],      [8,9,10]]
# gp_suc  = [[2,3,4] ,[5],[5,6,7],[7],  [8],[8,9,10], [10], [11],[11],  [11],            []]
#
# original_set = set([1,2,3,4,5,6,7,8,9,10,11])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("7) Project with 11 nodes, with three levels (three sons)")
# print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
# print(ct_ef, "\n")
#
#
# #8) Project with 14 nodes, with four levels (three sons)
# ct_due  = [0       ,  1,      1,  1,    1,       1,    1,    1,         1,     1,    1,   1,     1,              0]
# ct_es   = [0       ,  0,      0,  0,    1,       1,    1,    2,         2,     2,    3,   3,     3,        delta_n]
# ct_ef   = [0       ,  1,      1,  1,    2,       2,    2,    3,         3,     3,    4,   4,     4,        delta_n]
# ct_cfn  = [0       ,-20,      1,-20,    1,       1,    1,    1,         1,     1,    1,   1,     1,              0]
# ct_pred = [[14]    ,[1],    [1],[1],  [3],     [3],  [3],  [6],       [6],   [6],  [9], [9],   [9],             []]
# ct_suc  = [[2,3,4] , [],[5,6,7], [],   [],[8,9,10],   [],   [],[11,12,13],    [],   [],  [],    [],            [1]]
# gp_pred = [[]      ,[1],    [1],[1],[2,3],     [3],[3,4],[5,6],       [6], [6,7],[8,9], [9],[9,10],     [11,12,13]]
# gp_suc  = [[2,3,4] ,[5],[5,6,7],[7],  [8],[8,9,10], [10], [11],[11,12,13],  [13], [14],[14],  [14],             []]
#
# original_set = set([1,2,3,4,5,6,7,8,9,10,11,12,13,14])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("8) Project with 14 nodes, with four levels (three sons)")
# print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
# print(ct_ef, "\n")
#
#
# #9) Project with 17 nodes, with five levels (three sons)
# ct_due  = [0       , 1 ,      1,  1,    1,       1,    1,    1,          1,    1,   1,          1,     1,      1,         1,      1,         0]
# ct_es   = [0       , 0 ,      0,  0,    1,       1,    1,    2,          2,    2,   3,          3,     3,      4,         4,      4,   delta_n]
# ct_ef   = [0       , 1 ,      1,  1,    2,       2,    2,    3,          3,    3,   4,          4,     4,      5,         5,      5,   delta_n]
# ct_cfn  = [0       ,-20,      1,-20,    1,       1,    1,    1,          1,    1,   1,          1,     1,      1,         1,      1,         0]
# ct_pred = [[17]    ,[1],    [1],[1],  [3],     [3],  [3],  [6],        [6],  [6],  [9],       [9],   [9],   [12],      [12],   [12],        []]
# ct_suc  = [[2,3,4] , [],[5,6,7], [],   [],[8,9,10],   [],   [], [11,12,13],   [],   [],[14,15,16],    [],     [],        [],     [],       [1]]
# gp_pred = [[]      ,[1],    [1],[1],[2,3],     [3],[3,4],[5,6],        [6],[6,7],[8,9],       [9],[9,10],[11,12],      [12],[12,13],[14,15,16]]
# gp_suc  = [[2,3,4] ,[5],[5,6,7],[7],  [8],[8,9,10], [10], [11], [11,12,13], [13], [14],[14,15,16], [16],    [17],      [17],   [17],        []]
#
# original_set = set([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("9) Project with 17 nodes, with five levels (three sons)")
# print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
# print(ct_ef, "\n")
#
# #10) Project with 20 nodes, with six levels (three sons)
# ct_due  = [0       , 1 ,      1,  1,    1,       1,    1,    1,          1,    1,   1,          1,     1,      1,         1,      1,       1,    1,      1,              0]
# ct_es   = [0       , 0 ,      0,  0,    1,       1,    1,    2,          2,    2,   3,          3,     3,      4,         4,      4,       5,    5,      5,        delta_n]
# ct_ef   = [0       , 1 ,      1,  1,    2,       2,    2,    3,          3,    3,   4,          4,     4,      5,         5,      5,       6,    6,      6,        delta_n]
# ct_cfn  = [0       ,-20,      1,-20,    1,       1,    1,    1,          1,    1,   1,          1,     1,      1,         1,      1,       1,    1,      1,              0]
# ct_pred = [[20]    ,[1],    [1],[1],  [3],     [3],  [3],  [6],        [6],  [6],  [9],       [9],   [9],   [12],      [12],   [12],    [15], [15],   [15],             []]
# ct_suc  = [[2,3,4] , [],[5,6,7], [],   [],[8,9,10],   [],   [], [11,12,13],   [],   [],[14,15,16],    [],     [],[17,18,19],     [],      [],   [],     [],            [1]]
# gp_pred = [[]      ,[1],    [1],[1],[2,3],     [3],[3,4],[5,6],        [6],[6,7],[8,9],       [9],[9,10],[11,12],      [12],[12,13], [14,15], [15],[15,16],     [17,18,19]]
# gp_suc  = [[2,3,4] ,[5],[5,6,7],[7],  [8],[8,9,10], [10], [11], [11,12,13], [13], [14],[14,15,16], [16],    [17],[17,18,19],   [19],    [20], [20],   [20],             []]
#
# original_set = set([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
# total_Rec = 0
# total_Step3 = 0
# SA, DC = Step_3()
# print("10) Project with 20 nodes, with six levels (three sons)")
# print("Total of Step3: %d and total of Rec: %d" %(total_Step3, total_Rec))
# print(ct_ef, "\n")




global SS

SA_l_degree = [1,2,3,4,5,6,7,8,9]
SA_l = [5,9,2,3] # 7 VEZES
SA_l = [33,5,9,2,3,18,18,33] # 17 VEZES
SA_l = [33,5,9,2,3,18,18,33,33,0,45,92,500,13,17,80] # 46 VEZES
SA_l = [33,5,9,2,3,18,18,33,33,0,45,92,500,13,17,80,-3300,50,92,20,30,180,183,331,-133,10,145,392,-510,131,171,-801] # 121 VEZES !!!!!
SA_l = [33,5,9,2,3,18,18,33,33,0,45,92,500,13,17,80,-3300,50,92,20,30,180,183,331,-133,10,145,392,-510,131,171,-801,33,5,9,2,3,18,18,33,33,0,45,92,500,13,17,80,-3300,50,92,20,30,180,183,331,-133,10,145,392,-510,131,171,-801] # 271 VEZES !!!!!
SA_l = [21]
# SS = [-4000, 1000, 80000]
# SS = list(range(100))
SS = [10,15,16,20]
count_binary_insertion = 0
def binary_insertion(item, start, end):
    global count_binary_insertion
    count_binary_insertion += 1
    if len(SS) == 0:
        SS.append(item)
    else:
        middle = (start + end) // 2
        if start >= end:
            if end <= 0:
                if item > SS[0]:
                    SS.insert(1, item)
                else:
                    SS.insert(0, item)
            elif start >= len(SS):
                if item > SS[-1]:
                    SS.append(item)
                else:
                    SS.insert(len(SS), item)
            else:
                SS.insert(middle, item)

        elif item == SS[middle]:
            SS.insert(middle, item)
        elif (item > SS[middle]):
            start = middle + 1
            binary_insertion(item, start, end)
        elif (item < SS[middle]):
            end = middle - 1
            binary_insertion(item, start, end)

for item in SA_l:
    start = 0
    end = len(SS)
    binary_insertion(item, start, end)

print(SS)
print("'inserts_ordered' was executed %d vezes!" %(count))
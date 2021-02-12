# Title     : Batch ET, RS, SAA and HS
# Objective : Counting iterations and recursive calls
# Created by: Isac
# Created on: 17/10/2020

from ImportGraph import import_graph
from Early_tree_graph_refined import forward_pass
from RS.Recursive_search_original import main as RS_main
from SAA.SAA_original import main as SAA_main
from HS.Hybrid_search_original import main as HS_main
from os import listdir
from os.path import isfile, isdir, join
import pandas as pd
import time
import sys
sys.setrecursionlimit(190000)

# import igraph as ig

def Batch_ET_RS_SAA_HS(path, batch='TESTE'):
    global count

    pkg_graph = import_graph(path)

    #pkg_graph = import_graph('Samples/t')
    pkg_et_RS = {}
    pkg_et_SAA = {}
    pkg_et_HS = {}

    # Variables for count min and max nodes and edges
    min_nodes, max_nodes = 100000, 0
    min_nodes_file, max_nodes_file = None, None
    min_edges, max_edges = 100000, 0
    min_edges_file, max_edges_file = None, None

    #count = df_unique.shape[0]

    #i_SAA, i_HS, i_RS = df_SAA.shape[0], df_HS.shape[0], df_RS.shape[0]
    for i, current_file_graph in enumerate(pkg_graph.items()):
        #count += 1
        #i_SAA += 1
        #i_HS += 1
        #i_RS += 1

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

        # Call algorithms:
        algorithms = ["SAA", "HS", "RS"]
        for algorithm in algorithms:
            if algorithm == "SAA":
                et_SAA = forward_pass(original_graph, "SAA", current_file_name)
                # if et_SAA.deadline == 'G2':
                #     et_SAA.deadline = et_SAA.biggest_end + et_SAA.biggest_end * int(path.split('-')[-1])
                list_complement = list(SAA_main(et_SAA, original_graph))
            elif algorithm == "HS":
                et_HS = forward_pass(original_graph, "HS", current_file_name)
                list_complement = list(HS_main(et_HS, original_graph))
            else:
                # continue
                et_RS = forward_pass(original_graph, "RS", current_file_name)
                list_complement = list(RS_main(et_RS, original_graph))

            df_unique.loc[count] = [str(batch.split('-')[-6:]), current_file_name, algorithm] + \
                                [batch.split('-')[-6],
                                 batch.split('-')[-5],
                                 batch.split('-')[-4],
                                 batch.split('-')[-3],
                                 batch.split('-')[-2],
                                 batch.split('-')[-1]] + \
                                 list_complement
            count += 1

            # # # Criar objeto para leitura e selecionar planilha
            # file_reader = pd.ExcelFile(file_name_result)
            # file_writer = pd.ExcelWriter(file_name_result)
            # sheet_df = file_reader.parse("SAA_HS_RS")
            # sheet_df = pd.concat([sheet_df, df_unique]).drop_duplicates()
            # sheet_df.to_excel(file_writer, sheet="SAA_HS_RS", engine='openpyxl', index=False)
            # excel_writer.save()

            # # Loop para o caso de querer trabalhar com mais de uma planilha
            # for sheet in file_reader.sheet_names:
            #     sheet_df = file_reader.parse(sheet)
            #     # Concatenar com o que já existia
            #     if df_unique.get(sheet) is not None:
            #         sheet_df = pd.concat([sheet_df, df_unique]).drop_duplicates()
            #     # Gravar no arquivo
            #     sheet_df.to_excel(file_writer, sheet, engine='openpyxl', index=False)
            # # Salvar e fechar arquivo
            # #excel_writer.save()



############
#   MAIN   #
############

t1 = time.time()

paths = []

df_unique = pd.DataFrame(columns=
                         ['batch',
                          'instance',
                          'algo',
                          #############
                          'vertices',
                          'layer',
                          'fan',
                          'disRate',
                          'percNeg',
                          'cpMult',
                          #############
                          'g_vertices',
                          'g_edges',
                          'g_diameter',
                          'g_max in degree',
                          'g_min in degree',
                          'g_mean in degree',
                          'g_max out degree',
                          'g_min out degree',
                          'g_mean out degree',
                          'g_disRate',
                          'g_perc Negative',
                          'g_deadline',
                          'g_last task Early Finish',
                          'effort',
                          'NPV',
                          'time'])
#
# file_name_result = 'Samples/2020-12-26' + '/Result2020-12-27.xlsx'
# with pd.ExcelWriter(file_name_result) as excel_writer:
#     df_unique.to_excel(excel_writer, sheet_name='SAA_HS_RS', engine='openpyxl', index=False)
    #excel_writer.save()
#     #excel_writer.close()


#root_directory = 'C:/Users/Dell/PycharmProjects/untitled/Samples/2021-01-05/01-05-18-17-50-10-3-20-50-1'
#root_directory = 'C:/Users/Dell/PycharmProjects/Gerador_R/Samples/2021-01-21/01-21-19-09-80-20-3-30-50-2'
#root_directory = 'C:/Users/Dell/PycharmProjects/Gerador_R/Samples/2021-01-26/01-26-15-28-320-10-3-10-100-1'
root_directory = 'C:/Users/Dell/PycharmProjects/Gerador_R/Samples/2021-01-26/01-26-17-50-320-10-3-10-90-1'
root_directory = 'C:/Users/Dell/PycharmProjects/Gerador_R/Samples/2021-01-27_G130'
root_directory = 'C:/Users/Dell/PycharmProjects/Gerador_R/Samples/2021-01-28'
root_directory = 'C:/Users/Dell/PycharmProjects/Gerador_R/Samples/2021-01-28_pequena'
#root_directory = 'C:/Users/Dell/PycharmProjects/untitled/Samples/2020-12-29_official'
sub_directories = [d for d in listdir(root_directory) if isdir(join(root_directory, d))]
if len(sub_directories) == 0:
    paths.append(root_directory)
else:
    for current_sub_directory in sub_directories:
        paths.append(root_directory + '/' + current_sub_directory)

count = 0
for nr, path in enumerate(paths):
    #Batch_ET_RS_SAA_HS(path, path[14:])
    try:
        print('BATCH ' + str(nr) + '/' + str(len(paths)) + ': ' + path)
        Batch_ET_RS_SAA_HS(path, path)
    except Exception as e:
        print(e)

#file_name_result = 'Samples/2021-01-05' + '/Result2021-05-01_v2.xlsx'
# with pd.ExcelWriter(file_name_result) as excel_writer:
#     df_unique.to_excel(excel_writer, sheet_name='SAA_HS_RS', engine='openpyxl', index=False)

#file_name_result = 'Samples/2020-12-26' + '/Result2021-05-01_v2.csv'
#file_name_result = 'Samples/2021-01-21' + '/Result2021-21-01_Last_batch_ss.csv'
#file_name_result = 'Samples/2021-01-21' + '/Result2021-21-01_Last_batch_rec_itShift.csv'
#file_name_result = 'Samples/2021-01-21' + '/Result2021-21-01_Last_batch_rec_function_calls.csv'
#file_name_result_csv = 'Samples/2021-01-21' + '/Result2021-21-01_Last_batch.csv'
file_name_result_csv = 'Samples/2021-01-28' + '/Result2021-28-01_pequena.csv'
df_unique.to_csv(file_name_result_csv, sep=',', encoding='utf-8', index=False)

#file_name_result_csv = 'Samples/2021-01-21' + '/Result2021-21-01_Last_batch.xlsx'
file_name_result_xlsx = 'Samples/2021-01-28' + '/Result2021-28-01_pequena.xlsx'
with pd.ExcelWriter(file_name_result_xlsx) as excel_writer:
    df_unique.to_excel(excel_writer, sheet_name='SAA_HS_RS', engine='openpyxl', index=False)

# with pd.ExcelWriter('Samples/2020-12-26' + '/Result2020-12-27.xlsx') as writer:
#     df_unique.to_excel(writer, sheet_name='SAA_HS_RS', engine='openpyxl', index=False)
    # df_SAA.to_excel(writer, sheet_name='SAA', engine='openpyxl', index=False)
    # df_HS.to_excel(writer, sheet_name='HS', engine='openpyxl', index=False)
    # df_RS.to_excel(writer, sheet_name='RS', engine='openpyxl', index=False)


# paths.append('Samples/teste/t')
# for path in paths:
#     Batch_ET_RS_SAA_HS(path)

t2 = time.time()

print("Execution time: ", t2 - t1)
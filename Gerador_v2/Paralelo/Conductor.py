# # import os
# # from multiprocessing import Pool
import time


# #
# # jobs = ('job_1.py', 'job_2.py', 'job_3.py')
# # jobs = ('job_1.py', 'job_2.py')
# #
# # def run_process(job):
# #     os.system('python {}'.format(job))
# #
# #
# # pool = Pool(processes=2)
# # pool.map(run_process, jobs)
#
# #!/usr/bin/python
# from joblib import Parallel, delayed
# import threading
#
def bb():
    # t1 = time.time()
    for i in range(200000):
        print(i)
    # t2 = time.time()
    # print('\n Fim execução: ', t2 - t1)


#
# def minha_funcao2():
#     while
#
# #Parallel(n_jobs=4, verbose=1)(delayed(minha_funcao)() for i in range(2))
#
# #minha_funcao()
#
# t1 = threading.Thread(target=minha_funcao, args=())
# t1.start()
from Gerador_v2.Generator_vect_060221 import Bacth_Generator, Write_File
from concurrent.futures import ProcessPoolExecutor


def subprocess():
    t1 = time.time()
    pool = ProcessPoolExecutor(max_workers=2)
    r = pool.map(Bacth_Generator, [1])
    print(r)
    Write_File(r)
    t2 = time.time()
    print(t2 - t1)


subprocess()

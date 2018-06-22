from graph_generator import graph
from centrality_cpu import BFS_cpu
from centrality_gpu import BFS_gpu
import matplotlib.pyplot as plt
import time as time
import random as random
import numpy as np

if __name__ == '__main__':
    gpu_time = []
    cpu_time = []
    elements = [5,10,25,50,75,100]
    for i in elements:
        cur_graph = graph(1000 * i)
        cur_graph.create_for_each_k_edges(3)
        gpu_sol = BFS_gpu(cur_graph, 3)
        start = time.time()
        gpu_ans = gpu_sol.run()
        end = time.time()
        gpu_time.append(end-start)
        print(end-start)
        #cpu
        cpu_sol = BFS_cpu(cur_graph, 3)
        start = time.time()
        cpu_ans = cpu_sol.run()
        end = time.time()
        cpu_time.append(end-start)
        print(end-start)
        # check that results matches
        for j in range(len(gpu_ans)):
            if (gpu_ans[j] != cpu_ans[j]):
                print("Algorithms are not working correctly")
    print("Final results:")
    print(gpu_time)
    print(cpu_time)
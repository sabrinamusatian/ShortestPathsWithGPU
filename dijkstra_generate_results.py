from graph_generator import graph
from gpu_dijkstra import Dijkstra_gpu
from cpu_dijkstra import Dijkstra_cpu
import matplotlib.pyplot as plt
import time as time
import random as random

if __name__ == '__main__':
    gpu_time = []
    cpu_time = []
    for i in range(1,10):
        cur_graph = graph(2**20 * i)
        cur_graph.create_edges()
        src = random.randint(0, 2**20 * i)
        gpu_sol = Dijkstra_gpu(cur_graph)
        start = time.time()
        gpu_ans = gpu_sol.run(src)
        end = time.time()
        gpu_time.append(end-start)
        print(end-start)
        #cpu
        cpu_sol = Dijkstra_cpu(cur_graph)
        start = time.time()
        cpu_ans = cpu_sol.run(src)
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
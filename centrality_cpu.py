from graph_generator import graph
import numpy as np
max_val = 2 ** 20 * 10


class BFS_cpu:
    def __init__(self, graph, num_of_neib):
        self.gr = graph
        self.num_of_neib = num_of_neib

    def accumulate_closeness(self, dst):
        sum = 0
        for el in dst:
            c = self.gr.num_vert
            if el == max_val:
                c -= 1
            else:
                sum += el
        if c == 0:
            return 0
        else:
            return ((c - 1)**2/(self.gr.num_vert - 1)) / sum

    def run(self):
        num_vert = self.gr.num_vert
        centr = np.zeros(num_vert, dtype=np.int32)
        for vert in range(num_vert):
            src = vert
            dst = [max_val for i in range(num_vert)]
            dst[src] = 0
            flag = True
            d = 0
            while flag:
                flag = False
                for i in range(len(self.gr.start_edges)):
                    if dst[self.gr.start_edges[i]] == d:
                        if dst[self.gr.end_edges[i]] == max_val:
                            dst[self.gr.end_edges[i]] = d + 1
                            flag = True
                d = d + 1
            centr[vert] = self.accumulate_closeness(dst)
        return centr


if __name__ == '__main__':
    gr = graph(5)
    gr.create_for_each_k_edges(2)
    bfs = BFS_cpu(gr, 2)
    bfs.run()

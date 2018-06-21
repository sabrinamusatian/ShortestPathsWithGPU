from graph_generator import graph
import pickle
import random as random
max_val = 2**20 * 10

class Dijkstra_cpu:
    def __init__(self, graph):
       self.gr = graph

    def run(self):
        num_vert = self.gr.num_vert
        frontier = set()
        u = [True for i in range(num_vert)]
        dst = [max_val for i in range(num_vert)]
        src = random.randint(0, num_vert - 1)
        frontier.add(src)
        u[src] = False
        dst[src] = 0
        while True:
            # cpu: relax kernel
            while len(frontier) != 0:
                ver = frontier.pop()
                for edg in self.gr.edges[
                           self.gr.start_neib_idx[ver]:
                           self.gr.start_neib_idx[ver] + self.gr.ver_num_of_neib[ver]]:
                    dst[edg] = min(dst[edg], dst[ver] + 1)
            # cpu: minimum kernel
            min_val = max_val
            for i in range(num_vert):
                if u[i]:
                    min_val = min(min_val, dst[i] + 1)
            # terminating condition
            if (min_val == max_val):
                break
            # cpu: update kernel
            for i in range(num_vert):
                if u[i] and dst[i] < min_val:
                    u[i] = False
                    frontier.add(i)

if __name__ == '__main__':
    graph = graph(2**20)
    graph.create_edges()
    file = open("graph1.txt", 'wb')
    pickle.dump(graph, file)
    dsk = Dijkstra_cpu(graph)
    dsk.run()
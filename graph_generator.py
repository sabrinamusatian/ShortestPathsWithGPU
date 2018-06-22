import random as random
import numpy as np
# max_val = 2**20 * 10

class graph():
    def __init__(self, num_vert):
        self.edges = []
        self.start_edges = []
        self.end_edges = []
        self.ver_num_of_neib = np.zeros(num_vert, dtype=np.int32)
        self.num_vert = num_vert
        self.start_neib_idx = np.zeros(num_vert, dtype=np.int32)

    def create_edges(self):
        all_ver = [i for i in range(self.num_vert)]
        not_used = set(all_ver)
        for i in range(self.num_vert):
            num_of_neib = random.randint(3, 4)
            self.ver_num_of_neib[i] = num_of_neib
            self.start_neib_idx[i] = len(self.edges)
            for j in range(num_of_neib):
                if len(not_used) == 0:
                    not_used = set(all_ver)
                    some_ver = not_used.pop()
                else:
                    some_ver = not_used.pop()
                self.edges.append(some_ver)
        self.edges = np.array(self.edges, dtype=np.int32)

    def create_for_each_k_edges(self, num_of_neib):
        all_ver = [i for i in range(self.num_vert)]
        not_used = set(all_ver)
        for i in range(self.num_vert):
            self.ver_num_of_neib[i] = num_of_neib
            self.start_neib_idx[i] = len(self.edges)
            for j in range(num_of_neib):
                if len(not_used) == 0:
                    not_used = set(all_ver)
                    some_ver = not_used.pop()
                else:
                    some_ver = not_used.pop()
                self.start_edges.append(i)
                self.end_edges.append(some_ver)
        self.start_edges = np.array(self.start_edges, dtype=np.int32)
        self.end_edges = np.array(self.end_edges, dtype=np.int32)




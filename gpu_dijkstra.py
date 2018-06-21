from graph_generator import graph
import pickle
import random as random
import pyopencl as cl
import numpy as np

max_val = 2**20 * 10

class Dijkstra_gpu:
    def __init__(self, graph):
        self.gr = graph

    def run(self):
        num_vert = self.gr.num_vert
        front = np.empty(num_vert).astype(np.int32)
        u = np.empty(num_vert, dtype=np.int32)
        dst = np.empty(num_vert, dtype=np.int32)
        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)
        # parallel kernels
        init_kernel = cl.Program(ctx, """
            __kernel void initialize(__global int *front,
            __global int *u, __global int *dst)
            {
              int gid = get_global_id(0);
              front[gid] = 0;
              u[gid] = 1;
              dst[gid] = 10485760;
            }
            __kernel void relax(__global int *front,
            __global int *unsettled, __global int *dst,__global const int *edges,
            __global const int *start_neib_idx, __global const int *ver_num_of_neib)
            {
              int gid = get_global_id(0);
              if (front[gid] == 1){
                for (int i = start_neib_idx[gid]; i < start_neib_idx[gid] +
                 ver_num_of_neib[gid]; i++){
                    atom_min(&dst[edges[i]], dst[gid] + 1);
                }
              }
            }
            __kernel void minimum(__global int *dst,__global int *u, __global int *min_val)
            {
              int gid = get_global_id(0);
              if (u[gid] == 1){
                atom_min(min_val, dst[gid] + 1);
              }
            }
            __kernel void update(__global int *front,
            __global int *u, __global int *dst, __global int *min_val)
            {
              int gid = get_global_id(0);
              front[gid] = 0;
              if (u[gid] == 1 && dst[gid] < *min_val){
                    front[gid] = 1;
                    u[gid] = 0;
               }
            }
            """).build()
        # init kernel execution
        mf = cl.mem_flags
        front_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=front)
        u_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=u)
        dst_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=dst)
        init_kernel.initialize(queue, front.shape, None, front_buf, u_buf, dst_buf)
        queue.finish()
        cl.enqueue_copy(queue, front, front_buf)
        cl.enqueue_copy(queue, u, u_buf)
        cl.enqueue_copy(queue, dst, dst_buf)
        # choosing src
        src = random.randint(0, num_vert - 1)
        u[src] = 0
        dst[src] = 0
        front[src] = 1
        ed_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.gr.edges.astype(np.int32))
        ver_num_of_neib = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.gr.ver_num_of_neib.astype(np.int32))
        start_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.gr.start_neib_idx.astype(np.int32))
        while True:
            # gpu: relax kernel
            front_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=front)
            u_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=u)
            dst_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=dst)
            init_kernel.relax(queue, dst.shape, None, front_buf, u_buf, dst_buf, ed_buf, start_buf, ver_num_of_neib)
            queue.finish()
            cl.enqueue_copy(queue, dst, dst_buf)
            # gpu: minimum kernel
            min_val = max_val
            dst_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=dst)
            min_val_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=np.int32(min_val))
            init_kernel.minimum(queue, dst.shape, None, dst_buf, u_buf, min_val_buf)
            result = np.empty((1), dtype=np.int32)
            cl.enqueue_copy(queue, result, min_val_buf)
            # terminating condition
            min_val = result[0]
            if (min_val == max_val):
                break
            # gpu: update kernel
            min_val_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=np.int32(min_val))
            init_kernel.update(queue, front.shape, None, front_buf, u_buf, dst_buf, min_val_buf)
            queue.finish()
            cl.enqueue_copy(queue, front, front_buf)
            cl.enqueue_copy(queue, u, u_buf)







if __name__ == '__main__':
    graph = graph(5)
    graph.create_edges()
    file = open("graph1.txt", 'wb')
    pickle.dump(graph, file)
    dsk = Dijkstra_gpu(graph)
    dsk.run()
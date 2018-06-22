from graph_generator import graph
import pyopencl as cl
import numpy as np

max_val = 2 ** 20 * 10


class BFS_gpu:
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
            dst = np.empty(num_vert, dtype=np.int32)
            dst.fill(max_val)
            dst[src] = 0
            flag = 1
            d = 0
            ctx = cl.create_some_context()
            queue = cl.CommandQueue(ctx)
            init_kernel = cl.Program(ctx, """
                __kernel void bfs(__global int *start,
                __global int *end, __global int *dst, __global const int *max_val,
                __global const int *max_number, __global int *d, __global int *flag)
                {
                  int gid = get_global_id(0);
                  if (gid < *max_number){
                    if (dst[start[gid]] == *d){
                        if (dst[end[gid]] == *max_val){
                            *flag = 1;
                            dst[end[gid]] = *d + 1;
                        }
                    }
                  } 
                }
                """).build()
            mf = cl.mem_flags
            start_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.gr.start_edges.astype(np.int32))
            end_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.gr.end_edges.astype(np.int32))
            max_val_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.int32(max_val))
            max_num_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.int32(num_vert * self.num_of_neib))
            while flag == 1:
                flag = 0
                dst_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=dst)
                flag_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=np.int32(flag))
                d_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=np.int32(d))
                init_kernel.bfs(queue, self.gr.start_edges.shape, None,
                                start_buf, end_buf, dst_buf, max_val_buf, max_num_buf,
                                d_buf, flag_buf)
                result = np.empty((1), dtype=np.int32)
                cl.enqueue_copy(queue, result, flag_buf)
                flag = result[0]
                cl.enqueue_copy(queue, dst, dst_buf)
                d = d + 1
            centr[vert] = self.accumulate_closeness(dst)
        return centr


if __name__ == '__main__':
    gr = graph(40)
    gr.create_for_each_k_edges(2)
    bfs = BFS_gpu(gr, 2)
    bfs.run()

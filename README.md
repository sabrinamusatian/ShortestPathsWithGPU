##### Reimplementation of the algorithms from the following articles: 
* Hector Ortega-Arranz, Yuri Torres, Diego R. Llanos Ferraris, Arturo Gonzalez-Escribano "A New GPU-based Approach to the Shortest Path Problem"
* Ahmed Shamsul Arefin, Regina Berretta, Pablo Moscato "On Ranking Nodes using kNN Graphs, Shortest-paths and GPUs"

#### Requirments:
python 3, pyopencl, numpy, matplotlib

For comparasion with boost: boost library, c++

#### Hector Ortega-Arranz, Yuri Torres, Diego R. Llanos Ferraris, Arturo Gonzalez-Escribano "A New GPU-based Approach to the Shortest Path Problem"
Includes the Dijkstra algorithm both for CPU(cpu_dijkstra.py) and GPU(cpu_dijkstra.py)

For graph generation a helping script can be found in graph_generator.py. All of the graphs are generated in a way to be a connected graphs with the average degree of the vertices equal to 7.

The GPU algorithm was compared to both naive CPU implementation of dijkstra(cpu_dijkstra.py) and an advanced parallel implementation from boost library. Usage of the boost library for this experiment may be found in Boost Dijkstra folder.
The comparasion for CPU and GPU version has been performed with GPU: AMD Radeon R9 M370X and CPU: 2,8 GHz Intel Core i7 with the following results:
![Image of dijkstra results](https://github.com/sabrinamusatian/ShortestPathsWithGPU/blob/master/dijkstra_result.png)

#### Ahmed Shamsul Arefin, Regina Berretta, Pablo Moscato "On Ranking Nodes using kNN Graphs, Shortest-paths and GPUs"
Includes implementation for solving centrality problem. 

Due to the inability to use data from the original article, testing graphs were generate in the same manner as for the previous article(see graph_generator.py), but each of the vertices has exactly 3 neighbours(3 closest neighbours as per the original article, since there KNN trees were built).

The core idea of the algorithm is to use BFS to search for the all shortest distances from one vertice and then perform this operation for every vertice. As part of the experiment the GPU solution was compared to naive CPU implementation of this algorithm. The speedups from this experiment may be seen below: 
![Image of centra speedup results](https://github.com/sabrinamusatian/ShortestPathsWithGPU/blob/master/centrality_speedup_results.png)

Also the idea of the algorithm was applied for the Dijkstra CPU implementation from the Boost library(take shortest paths from one vertice and perform experiment for every vertice). Code for using Boost library may be found at Boost Dijkstra folder. GPU implementation may be found at (centrality_gpu.py) and naive CPU(centrality_cpu.py). The results of comparasion are the following
![Image of centra results](https://github.com/sabrinamusatian/ShortestPathsWithGPU/blob/master/centrality_results.png)




Reimplementation of the algorithms from the following articles: 
* Hector Ortega-Arranz, Yuri Torres, Diego R. Llanos Ferraris, Arturo Gonzalez-Escribano "A New GPU-based Approach to the Shortest Path Problem"
* Ahmed Shamsul Arefin, Regina Berretta, Pablo Moscato "On Ranking Nodes using kNN Graphs, Shortest-paths and GPUs"

####Requirments:
python 3, pyopencl, numpy, matplotlib
#### Hector Ortega-Arranz, Yuri Torres, Diego R. Llanos Ferraris, Arturo Gonzalez-Escribano "A New GPU-based Approach to the Shortest Path Problem"
Includes the Dijkstra algorithm both for CPU(cpu_dijkstra.py) and GPU(cpu_dijkstra.py)

For graph generation a helping script can be found in graph_generator.py

The comparasion for CPU and GPU version has been performed with GPU: AMD Radeon R9 M370X and CPU: 2,8 GHz Intel Core i7 with the following results:
![Image of dijkstra results](https://github.com/sabrinamusatian/ShortestPathsWithGPU/blob/master/dijkstra_results.png)

#### Ahmed Shamsul Arefin, Regina Berretta, Pablo Moscato "On Ranking Nodes using kNN Graphs, Shortest-paths and GPUs"
Includes implementation for solving centrality problem. Due to the inability to use data from the original article, testing graphs were generate in the same manner as for the previous article(see graph_generator.py).
![Image of centra results](https://github.com/sabrinamusatian/ShortestPathsWithGPU/blob/master/centrality_results.png)
![Image of centra speedup results](https://github.com/sabrinamusatian/ShortestPathsWithGPU/blob/master/centrality_speedup_results.png)



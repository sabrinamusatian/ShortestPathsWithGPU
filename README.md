Reimplementation of the algorithms from the following articles: 
* Hector Ortega-Arranz, Yuri Torres, Diego R. Llanos Ferraris, Arturo Gonzalez-Escribano "A New GPU-based Approach to the Shortest Path Problem"
* Ahmed Shamsul Arefin, Regina Berretta, Pablo Moscato "On Ranking Nodes using kNN Graphs, Shortest-paths and GPUs"

#### Hector Ortega-Arranz, Yuri Torres, Diego R. Llanos Ferraris, Arturo Gonzalez-Escribano "A New GPU-based Approach to the Shortest Path Problem"
Includes the Dijkstra algorithm both for CPU(cpu_dijkstra.py) and GPU(cpu_dijkstra.py)
For graph generation a helping script can be found in graph_generator.py
The comparasion for CPU and GPU version has been performed with GPU: AMD Radeon R9 M370X and CPU: 2,8 GHz Intel Core i7 with the following results:
![Image of dijkstra results](https://github.com/sabrinamusatian/ShortestPathsWithGPU/blob/master/gpu_dijkstra.py)



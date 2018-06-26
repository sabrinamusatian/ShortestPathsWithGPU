#include <iostream>
#include <fstream>
#include <boost/config.hpp>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>
#include <boost/property_map/property_map.hpp>
#include <boost/graph/iteration_macros.hpp>
#include <boost/graph/properties.hpp>


#include <iostream>
#include <utility>
#include <vector>
#include <chrono>

using namespace std::chrono;
using namespace boost;

// This path needs to be adjusted accordingy with the user path
std::string base_path = "/Users/sabrina/CLionProjects/dijkstra_boost/data_dijkstra/";
std::string base_centrality_path = "/Users/sabrina/CLionProjects/dijkstra_boost/data_centrality/";
typedef adjacency_list <listS, vecS, directedS,
no_property, property<edge_weight_t, int>> graph_t;
typedef graph_traits<graph_t>::vertex_descriptor vertex_descriptor;
typedef graph_traits<graph_t>::edge_descriptor edge_descriptor;
typedef std::pair<int, int> Edge;
Edge edge_array[33029244];
long long weights[33029244];

void measure_dijkstra(){
    std::string graphs_names[] = {"graph1.txt", "graph2.txt", "graph3.txt", "graph4.txt", "graph5.txt", "graph6.txt",
                                  "graph7.txt", "graph8.txt", "graph9.txt"};
    std::string src_names[] = {"src1.txt", "src2.txt", "src3.txt", "src4.txt", "src5.txt", "src6.txt", "src7.txt",
                               "src8.txt", "src9.txt"};

    for (int num_gr = 0; num_gr < 9; num_gr++) {
        long long num_nodes, num_edges;
        //std::ifstream fin(base_path + "graph1.txt");
        std::ifstream fin(base_path + graphs_names[num_gr]);
        fin >> num_nodes >> num_edges;
        for (long long ed = 0; ed < num_edges; ed++) {
            long long a, b;
            fin >> a >> b;
            edge_array[ed] = Edge(a, b);
            weights[ed] = 1;
        }
        int num_arcs = num_edges;
        graph_t g(edge_array, edge_array + num_arcs, weights, num_nodes);
        property_map<graph_t, edge_weight_t>::type weightmap = get(edge_weight, g);
        std::vector<vertex_descriptor> p(num_vertices(g));
        std::vector<int> d(num_vertices(g));
        fin.close();
        std::ifstream fsrc(base_path + src_names[num_gr]);
        long long src;
        fsrc >> src;
        vertex_descriptor s = vertex(src, g);
        high_resolution_clock::time_point t1 = high_resolution_clock::now();
        dijkstra_shortest_paths(g, s, predecessor_map(&p[0]).distance_map(&d[0]));
        high_resolution_clock::time_point t2 = high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>(t2 - t1).count();
        std::cout << duration << std::endl;
    }
}

void measure_centrality(){
    std::string graphs_names[] = {"graph5.txt", "graph10.txt", "graph25.txt", "graph50.txt"};

    for (int num_gr = 0; num_gr < 9; num_gr++) {
        long long num_nodes, num_edges;
        std::ifstream fin(base_centrality_path + graphs_names[num_gr]);
        fin >> num_nodes >> num_edges;
        for (long long ed = 0; ed < num_edges; ed++) {
            long long a, b;
            fin >> a >> b;
            edge_array[ed] = Edge(a, b);
            weights[ed] = 1;
        }
        int num_arcs = num_edges;
        graph_t g(edge_array, edge_array + num_arcs, weights, num_nodes);
        property_map<graph_t, edge_weight_t>::type weightmap = get(edge_weight, g);
        std::vector<vertex_descriptor> p(num_vertices(g));
        std::vector<int> d(num_vertices(g));
        high_resolution_clock::time_point t1 = high_resolution_clock::now();
        for (long long src = 0; src < num_nodes; src++) {
            vertex_descriptor s = vertex(src, g);
            dijkstra_shortest_paths(g, s, predecessor_map(&p[0]).distance_map(&d[0]));
        }
        high_resolution_clock::time_point t2 = high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>(t2 - t1).count();
        std::cout << duration << std::endl;
    }
}

int main() {
    measure_centrality();
    return EXIT_SUCCESS;
}
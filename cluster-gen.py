import random

def generate_clustered_graph_data(num_nodes, num_clusters):
    graph_data = {'num_nodes': num_nodes, 'nodes': []}
    total_edges = 0
    cluster_size = num_nodes // num_clusters
    #avg_cluster_size = 

    clusters = []
    for i in range(num_clusters):
        cluster = list(range(i * cluster_size + 1, (i + 1) * cluster_size + 1))
        clusters.append(cluster)

    # Add random connections within each cluster
    for cluster in clusters:
        for node in cluster:
            rand_modifier = random.randint(-abs(cluster_size//10), cluster_size//10)
            curr_cluster = cluster_size + rand_modifier
            num_parents = min(curr_cluster, len(cluster) - 1)
            parents = random.sample([n for n in cluster if n != node], num_parents)

            parents.extend(random.sample(range(1, num_nodes + 1), random.randint(1,10)%4))
            #if i + 1 in parents:
            #    parents.remove(i + 1)
            graph_data['nodes'].append({'parents': parents})
            total_edges += num_parents


    # Print the average number of edges per node
    print("Total Edges:", total_edges)
    return graph_data


def generate_output_file(filename, graph_data):
    with open(filename, 'w') as file:
        # Write the number of nodes in the graph
        file.write(str(graph_data['num_nodes']) + '\n')

        # Write the parent information for each node
        for node in graph_data['nodes']:
            parents = ' '.join(map(str, node['parents']))
            file.write(f"{len(node['parents'])} {parents}\n")



for i in range(1,5):
    output_file_name = f'test/input/{i}-medium-cluster.in'
    generate_output_file(output_file_name, generate_clustered_graph_data(1000, 5))

import random


def generate_random_graph_data(num_nodes):
    graph_data = {'num_nodes': num_nodes, 'nodes': []}
    total_edges = 0

    for i in range(num_nodes):
        # Generate random number of parents for each node (between 0 and num_nodes - 1)
        max_parents = 20
        num_parents = random.randint(0, min(num_nodes - 1, max_parents))
        total_edges += num_parents

        # Generate a list of unique random parents (between 1 and num_nodes), preventing self-loops
        parents = random.sample(range(1, num_nodes + 1), num_parents)
        if i + 1 in parents:
            parents.remove(i + 1)

        # Add the node to the graph data
        graph_data['nodes'].append({'parents': parents})

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



for i in range(1,2):
    output_file_name = f'test/input/{i}-large-random.in'
    generate_output_file(output_file_name, generate_random_graph_data(10000))

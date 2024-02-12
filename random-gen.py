import random


def generate_random_graph_data(num_nodes):
    graph_data = {'num_nodes': num_nodes, 'nodes': []}

    for _ in range(num_nodes):
        # Generate random number of parents for each node (between 0 and num_nodes - 1)
        max_parents = 25
        num_parents = random.randint(0, min(num_nodes - 1, max_parents))

        # Generate a list of unique random parents
        parents = random.sample(range(1, num_nodes + 1), num_parents)

        # Add the node to the graph data
        graph_data['nodes'].append({'parents': parents})

    return graph_data


def generate_output_file(filename, graph_data):
    with open(filename, 'w') as file:
        # Write the number of nodes in the graph
        file.write(str(graph_data['num_nodes']) + '\n')

        # Write the parent information for each node
        for node in graph_data['nodes']:
            parents = ' '.join(map(str, node['parents']))
            file.write(f"{len(node['parents'])} {parents}\n")


generate_output_file('output.txt', generate_random_graph_data(100000))

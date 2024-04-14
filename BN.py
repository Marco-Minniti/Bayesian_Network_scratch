import numpy as np

class Node:
    def __init__(self, parents, probs):
        self.parents = parents
        self.probs = probs

# Creo la classe Network che contiene i nodi e i metodi per calcolare la probabilità di un evento 
class Network:
    def __init__(self, net):
        self.net = net

    def topological_sort(self):
        visited = set()
        topo_order = []
        def visit(node_name):
            if node_name in visited:
                return
            visited.add(node_name)
            for parent in self.net[node_name].parents:
                visit(parent)
            topo_order.append(node_name)
        for node_name in self.net:
            visit(node_name)
        return topo_order

    def sample_node(self, node, evidence): 
        probs = node.probs # probabilità del nodo selezionato
        
        parents_values=[]
        if len(node.parents) > 1:
            for parent in node.parents: # scorro i genitori del nodo selezionato (il primo viene skippato perchè non ha genitori)
                parents_values.append(evidence[parent])
            probs = node.probs[tuple(parents_values)] # prendo le probabilità del nodo selezionato
        else:
            if len(node.parents) == 1:
                for parent in node.parents:
                    probs = node.probs[evidence[parent]]
        return np.random.choice(list(probs.keys()), p=list(probs.values())) # scelgo casualmente tra le chiavi (del dizionario probs).....in base alle probabilità specificate dai valori. (ricordo che la lista scelta da dove estrarre la chiave dipende dal valore assunto dal padre)

    def ancestral_sampling(self):
        evidence = {}
        sampled_nodes = {}
        topo_order = self.topological_sort()  # Add this line to get the topological order
        for node_name in topo_order:  # Iterate over nodes in topological order
            node = self.net[node_name]
            sampled_value = self.sample_node(node, evidence)
            sampled_nodes[node_name] = sampled_value
            evidence[node_name] = sampled_value
        return sampled_nodes






# Ordered net
# net = {
#     'Alarm': Node([], {'yes': 0.9, 'no': 0.1}),
#     'Wakeup': Node([], {'early': 0.5, 'late': 0.5}),

#     'Breakfast': Node(['Wakeup', 'Alarm'], {('early', 'yes'): {'yes': 0.9, 'no': 0.1}, ('early', 'no'): {'yes': 0.9, 'no': 0.1}, ('late', 'yes'): {'yes': 0.6, 'no': 0.4}, ('late', 'no'): {'yes': 0.6, 'no': 0.4}}),
#     'Toilet': Node(['Breakfast'], {('yes'): {'quick': 0.7, 'slow': 0.3}, ('no'): {'quick': 0.4, 'slow': 0.6}}),
#     'Shower': Node(['Breakfast', 'Toilet'], {('yes', 'quick'): {'quick': 0.9, 'slow': 0.1}, ('yes', 'slow'): {'quick': 0.7, 'slow': 0.3}, ('no', 'quick'): {'quick': 0.6, 'slow': 0.4}, ('no', 'slow'): {'quick': 0.4, 'slow': 0.6}}),
    
#     'Work': Node(['Shower'], {('quick'): {'productive': 0.9, 'unproductive': 0.1}, ('slow'): {'productive': 0.6, 'unproductive': 0.4}}),
    
#     'Lunch': Node(['Work'], {('productive'): {'healthy': 0.7, 'unhealthy': 0.3}, ('unproductive'): {'healthy': 0.4, 'unhealthy': 0.6}}),
    
#     'Meeting': Node(['Lunch'], {('healthy'): {'yes': 0.8, 'no': 0.2}, ('unhealthy'): {'yes': 0.4, 'no': 0.6}}),
#     'Sport': Node(['Work', 'Meeting'], {('productive', 'yes'): {'yes': 0.9, 'no': 0.1}, ('productive', 'no'): {'yes': 0.6, 'no': 0.4}, ('unproductive', 'yes'): {'yes': 0.7, 'no': 0.3}, ('unproductive', 'no'): {'yes': 0.4, 'no': 0.6}}),
    
#     'Dinner': Node(['Lunch', 'Sport'], {('healthy', 'yes'): {'healthy': 0.9, 'unhealthy': 0.1}, ('healthy', 'no'): {'healthy': 0.6, 'unhealthy': 0.4}, ('unhealthy', 'yes'): {'healthy': 0.7, 'unhealthy': 0.3}, ('unhealthy', 'no'): {'healthy': 0.4, 'unhealthy': 0.6}}),
# }

# Shuffle net
net = {

    'Dinner': Node(['Lunch', 'Sport'], {('healthy', 'yes'): {'healthy': 0.9, 'unhealthy': 0.1}, ('healthy', 'no'): {'healthy': 0.6, 'unhealthy': 0.4}, ('unhealthy', 'yes'): {'healthy': 0.7, 'unhealthy': 0.3}, ('unhealthy', 'no'): {'healthy': 0.4, 'unhealthy': 0.6}}),
    'Alarm': Node([], {'yes': 0.9, 'no': 0.1}),
    'Breakfast': Node(['Wakeup', 'Alarm'], {('early', 'yes'): {'yes': 0.9, 'no': 0.1}, ('early', 'no'): {'yes': 0.9, 'no': 0.1}, ('late', 'yes'): {'yes': 0.6, 'no': 0.4}, ('late', 'no'): {'yes': 0.6, 'no': 0.4}}),
    'Toilet': Node(['Breakfast'], {('yes'): {'quick': 0.7, 'slow': 0.3}, ('no'): {'quick': 0.4, 'slow': 0.6}}),
    'Work': Node(['Shower'], {('quick'): {'productive': 0.9, 'unproductive': 0.1}, ('slow'): {'productive': 0.6, 'unproductive': 0.4}}),
    'Meeting': Node(['Lunch'], {('healthy'): {'yes': 0.8, 'no': 0.2}, ('unhealthy'): {'yes': 0.4, 'no': 0.6}}),
    'Sport': Node(['Work', 'Meeting'], {('productive', 'yes'): {'yes': 0.9, 'no': 0.1}, ('productive', 'no'): {'yes': 0.6, 'no': 0.4}, ('unproductive', 'yes'): {'yes': 0.7, 'no': 0.3}, ('unproductive', 'no'): {'yes': 0.4, 'no': 0.6}}),
    'Wakeup': Node([], {'early': 0.5, 'late': 0.5}),
    'Lunch': Node(['Work'], {('productive'): {'healthy': 0.7, 'unhealthy': 0.3}, ('unproductive'): {'healthy': 0.4, 'unhealthy': 0.6}}),
    'Shower': Node(['Breakfast', 'Toilet'], {('yes', 'quick'): {'quick': 0.9, 'slow': 0.1}, ('yes', 'slow'): {'quick': 0.7, 'slow': 0.3}, ('no', 'quick'): {'quick': 0.6, 'slow': 0.4}, ('no', 'slow'): {'quick': 0.4, 'slow': 0.6}}),
    
}

network = Network(net)
topo_order = network.topological_sort()

# for _ in range(10):
#     print(network.ancestral_sampling())


# Verifico che la probabilità calcolata con il metodo di ancestral sampling sia simile a quella calcolata teoricamente
def prob_empirical():
    count = 0
    for _ in range(10000):
        sampled_nodes = network.ancestral_sampling()
        if sampled_nodes['Dinner'] == 'unhealthy':
            count += 1
    return count / 10000

print(prob_empirical())
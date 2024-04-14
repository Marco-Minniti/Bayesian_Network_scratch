import numpy as np


class Node:
    def __init__(self, parents, probs):
        self.parents = parents
        self.probs = probs


# Definizione dei nodi
nodes = {
    
    'Alarm': Node([], {'yes': 0.9, 'no': 0.1}),

    'Coffee': Node(['Wakeup', 'Alarm'], {('early', 'yes'): {'yes': 0.9, 'no': 0.1}, ('early', 'no'): {'yes': 0.9, 'no': 0.1}, ('late', 'yes'): {'yes': 0.6, 'no': 0.4}, ('late', 'no'): {'yes': 0.6, 'no': 0.4}}),
    #'Coffee': Node(['Wakeup'], {('early'): {'yes': 0.9, 'no': 0.1}, ('late'): {'yes': 0.6, 'no': 0.4}}), # (CPT) Se il nodo genitore ha valore 'early', la probabilità di avere 'yes' è 0.9, altrimenti è 0.1, se il nodo genitore ha valore 'late', la probabilità di avere 'yes' è 0.6, altrimenti è 0.4
    'Toilet': Node(['Coffee'], {('yes'): {'quick': 0.7, 'slow': 0.3}, ('no'): {'quick': 0.4, 'slow': 0.6}}),
    

    'Lunch': Node(['Study'], {('productive'): {'healthy': 0.7, 'unhealthy': 0.3}, ('unproductive'): {'healthy': 0.4, 'unhealthy': 0.6}}),

    'Wakeup': Node([], {'early': 0.5, 'late': 0.5}),
    'Dinner': Node(['Exercise', 'Study'], {('yes', 'productive'): {'healthy': 0.9, 'unhealthy': 0.1}, ('yes', 'unproductive'): {'healthy': 0.6, 'unhealthy': 0.4}, ('no', 'productive'): {'healthy': 0.7, 'unhealthy': 0.3}, ('no', 'unproductive'): {'healthy': 0.4, 'unhealthy': 0.6}}),

    'Study': Node(['Toilet'], {('quick'): {'productive': 0.8, 'unproductive': 0.2}, ('slow'): {'productive': 0.6, 'unproductive': 0.4}}),
    'Exercise': Node(['Lunch'], {('healthy'): {'yes': 0.8, 'no': 0.2}, ('unhealthy'): {'yes': 0.4, 'no': 0.6}}),
    
    
    # Aggiungere altri 5 nodi 
}

def topological_sort(nodes):
    visited = set()
    topo_order = []
    def visit(node_name):
        if node_name in visited:
            return
        visited.add(node_name)
        for parent in nodes[node_name].parents:
            visit(parent)
        topo_order.append(node_name)
    for node_name in nodes:
        visit(node_name)
    return topo_order


def sample_node(node, evidence): 
    probs = node.probs # probabilità del nodo selezionato
    
    parents_values=[]
    if len(node.parents) > 1:
        for parent in node.parents: # scorro i genitori del nodo selezionato (il primo viene skippato perchè non ha genitori)
            parents_values.append(evidence[parent])
        probs = node.probs[tuple(parents_values)] # prendo le probabilità del nodo selezionato in base al valore assunto dal genitore nell'iterazione precedente
        # PROBLEMA: QUANDO NELLA LISTA CI SONO EFFETTIVAMENTE PIU' DI 1 ELEMENTO FUNZIONA E CREA LA TUPLA CORRETTAMENTE, MA QUANDO C'E' UN SOLO ELEMENTO CREA (elemento,) INVECE DI (elemento)
    else:
        if len(node.parents) == 1:
            for parent in node.parents:
                probs = node.probs[evidence[parent]]
    return np.random.choice(list(probs.keys()), p=list(probs.values())) # scelgo casualmente tra le chiavi (del dizionario probs).....in base alle probabilità specificate dai valori. (ricordo che la lista scelta da dove estrarre la chiave dipende dal valore assunto dal padre)

def ancestral_sampling(nodes):
    sample = {} # dizionario restituito in output
    for node_name, node_values in nodes.items(): # scorre tutti i nodi
        if node_name not in sample: # inutile, sempre vera perchè reti bayesiane sono sempre dei DAG
            sample[node_name] = sample_node(node_values, sample) # costruisce man mano il dizionario in output { nodo: valore derivante dalla probabilità }
    return sample




topo_order = topological_sort(nodes)
ordered_nodes = {node_name: nodes[node_name] for node_name in topo_order}

for _ in range(10):
    print(ancestral_sampling(ordered_nodes))

# print(ancestral_sampling(ordered_nodes))



# for _ in range(10):
#     print(ancestral_sampling(nodes))

# print(ancestral_sampling(nodes))



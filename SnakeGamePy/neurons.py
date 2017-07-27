"""
A NEAT-based neural network system
    written by Yovel Key-Cohen
    with help from Jeffrey Holzman
"""

import activation_functions
rand = random
import random

INPUT_COUNT = 256  # Global number of inputs
OUTPUT_COUNT = 1  # Global number of outputs
MAX_SEX_MULTIPLIER = 4  # Maximum number of times a species can have sex, multiplied by generation number
MIN_SEX_MULTIPLIER = 2  # Minimum sex
ACTIVATION_FUNCTION = activation_functions.tanh
GENOME_DISTANCE_THRESHOLD = 7  # Unknown exactly what the outputs for genome distance will be, but this determines how different a genome is before being classified as a new species

global_innovation_number = 0  # Tracks when mutations occur - two genomes will have the same innovation number if they make it at the same time, although it may not be the same mutation event


def rand_floats(n, m):
    """Gets random floats between n and m, nd being the amount to get"""
    return rand(n, m)
    #return n * 2 * random.random() + m


"""The global population tracker"""
class Population:
    def __init__(self):
        self.species = []
    def new_species(self, father=None, mother=None):
        """Wrapper for species creation"""
        self.species.append(Species(father, mother, self))
    def generation(self):
        """Increments global_innovation_number, applies mutations, force sex"""
        global global_innovation_number
        for species in self.species:
            species.generation_elapse()
        global_innovation_number += 1
        self.kill_poor_species()
    def kill_poor_species(self):
        """Removes the lowest species when there's beginning to be too much variation - maybe switch to killing those lower than mean fitness"""
        for species in self.species:
            species.update_fitness()
        self.species.sort(key=lambda s: s.average_fitness)
        if len(self.species) > 7:
            del self.species[:len(self.species)/3]


"""Tracker for a species of organisms"""
class Species:
    def __init__(self, father, mother, population):
        if father is mother is None:  # Random starting nodes
            father = Network()
            mother = Network()
        father.link_mutate()
        mother.link_mutate()
        self.current_generation = [father, mother]
        self.generation = 1
        self.father = father
        self.mother = mother
        self.average_fitness = 0
        self.population = population

    @staticmethod
    def gdistance(n1, n2):
        """Gets genome distance between n1 and n2"""
        # Coefficients
        c1 = 1
        c2 = 1
        c3 = 1

        # Finding stats for largest and smallest networks by genome size
        n1s = len(n1.hidden_nodes + n1.connections)
        n2s = len(n2.hidden_nodes + n2.connections)
        largest = n1 if n1s < n2s else n2
        smallest = n1 if n1s > n2s else n2
        largest.sum = n1s if n1s < n2s else n2s
        smallest.sum = n1s if n1s > n2s else n2s
        excess = disjoint = 0

        # Finding disjoint and excess gene count
        for i in range(len(largest.hidden_nodes)):
            try:
                if largest.hidden_nodes[i].gene_id != smallest.hidden_nodes[i].gene_id:
                    disjoint += 1
            except IndexError:
                excess += 1

        # Finding the total absolute difference in connection weights by inno
        weight_diff_sum = 0
        for i in range(len(largest.connections)):
            try:
                weight_diff_sum += abs(smallest.connections[i].weight - largest.connections[i].weight)
            except IndexError:
                break

        # Return genome distance
        distance = (((c1 * excess) + (c2 * disjoint)) / largest.sum) + (c3 * weight_diff_sum)
        #del largest.sum, smallest.sum
        return distance

    def update_fitness(self):
        """Update mean species fitness by those of its networks"""
        l = list([n.fitness for n in self.current_generation])
        self.average_fitness = sum(l) / len(l)

    def generation_elapse(self):
        """Lets a generation elapse in the species"""
        # Kill off the weaklings
        del sorted(self.current_generation, key=lambda n: n.fitness)[:len(self.current_generation)/3]
        # Have sex - possible to not create any new beings, in which case the old generation sticks around without its weaker ones
        new_generation = [
            Network.child(random.choice(self.current_generation), random.choice(self.current_generation))
            for _ in range(self.generation * random.randint(MIN_SEX_MULTIPLIER, MAX_SEX_MULTIPLIER))
            ]
        # Check if they didn't have sex
        if new_generation:
            self.current_generation = new_generation
        # Mutate the new generation for variety
        self.mutate_generation()
    def mutate_generation(self):
        """Applies a random mutation to every creature except the fittest"""
        self.current_generation.sort(key=lambda n: n.fitness)
        for network in self.current_generation[1:]:
            network.random_mutate()
    def distance_check(self):
        """Speciates those organisms that are far enough away from their ancestors in genomic distance"""
        for network in self.current_generation:
            if Species.gdistance(network, self.father) > GENOME_DISTANCE_THRESHOLD:
                self.current_generation.remove(network)
                closest_match = sorted(self.current_generation, key=lambda n2: Species.gdistance(network, n2))[0]
                self.current_generation.remove(closest_match)
                self.population.new_species(network, closest_match)

"""A Neural Network"""
class Network:
    def __init__(self):
        self.fitness = 0
        self.input_nodes = [Node()] * INPUT_COUNT
        self.hidden_nodes = []
        self.output_nodes = [Node()] * OUTPUT_COUNT
        self.connections = []
        self.conn_dict = dict()

    @staticmethod
    def child(father, mother):
        """Creates a child network that is a combination of father and mother networks"""
        # Finds the strongest parent by fitness
        strong = max(father, mother, key=lambda n: n.fitness)
        weak = min(father, mother, key=lambda n: n.fitness)
        child_conndict = dict()
        child_input = strong.input_nodes
        child_output = strong.output_nodes

        # Randomly selects genes if they're the same inno - disjoint and excess are pulled from strongest parent
        wconns = list(sorted(weak.connections, key=lambda c: c.gene_ids[0]))
        sconns = list(sorted(strong.connections, key=lambda c: c.gene_ids[0]))
        for i in range(len(sconns)):
            if sconns[i].gene_ids == wconns[i].gene_ids:
                child_conndict[sconns[i].gene_ids] = random.choice([sconns[i], wconns[i]])
            else:
                child_conndict[sconns[i].gene_ids] = sconns[i]

        #
        child = Network()
        child.input_nodes = child_input
        child.output_nodes = child_output
        child.conn_dict = child_conndict
        child.connections = child_conndict.values()
        child.hidden_nodes = []
        for c in child.connections:
            if c.node1 not in child.hidden_nodes and c.node1 not in child.input_nodes:
                child.hidden_nodes.append(c.node1)
            if c.node2 not in child.hidden_nodes and c.node2 not in child.output_nodes:
                child.hidden_nodes.append(c.node2)
        child.hidden_nodes.sort(key=lambda c: c.gene_id)
        return child

    def configure_nodex(self):
        """Configuring the x value of a node - also removes any detected loops in the network (unknown whether that part works or not)"""
        for node in self.output_nodes:  # Outputs are x = 255 (hopefully hidden layer doesn't reach 255 in x)
            node.x = 100000000000000
        for node in self.input_nodes:  # Inputs are x = 0
            node.x = 0
        for i in range(len(self.connections)):  # Fixes loops, hopefully
            conn = self.connections[i]
            if conn.node2.x == -1:
                conn.node2.x = conn.node1.x + 1
            elif conn.node1.x > conn.node2.x:
                del self.connections[i]

    def random_mutate(self, point=0.00, link=0.80, node=0.00, useable=0.20):
        """Selects a random mutation to apply by probability in hundredths"""
        probabilities = [self.point_mutate] * int(point * 100)\
                        + [self.link_mutate] * int(link * 100)\
                        + [self.node_mutate] * int(node * 100)\
                        + [self.useable_mutate] * int(useable * 100)
        random.choice(probabilities)()
        return self

    def feed_forward(self, inputs):
        """Accepts input of length input_nodes, returns output of length output_nodes"""
        output = []
        _input = inputs[:len(self.input_nodes)]
        for node in range(len(self.input_nodes)):
            self.input_nodes[node].t_input = _input[node]
            self.input_nodes[node].output = lambda: node.t_input
        for node in self.output_nodes:
            output.append(node.output())
        return output

    def iho_choice(self, n=None):
        """Function for getting a random node list - input, hidden, or output"""
        if n is None:
            n = random.choice([1,2,3])
        elif isinstance(n, list):
            n = random.choice([1,2,3])
        if n == 1:
            return self.input_nodes
        elif n == 2:
            return self.hidden_nodes
        else:
            return self.output_nodes
    def point_mutate(self):
        """A mutation type that randomizes the weight of a connection"""
        random.choice(self.connections).randomize_weight()
        return 0
    def link_mutate(self):
        """A mutation type that creates a random connection in the network"""
        if self.hidden_nodes:
            t1 = random.choice([1, 2])
            t2 = random.choice([2, 3])
            n1 = ''
            n2 = ''
            if t1 == 1:
                n1 = random.choice(self.input_nodes)
            elif t1 == 2:
                n1 = random.choice(self.hidden_nodes)
            if t2 == 2:
                n2 = random.choice(self.hidden_nodes)
            elif t2 == 3:
                n2 = random.choice(self.output_nodes)
        else:
            n1 = random.choice(self.input_nodes)
            n2 = random.choice(self.output_nodes)
        self.new_conn(n1, n2)
        return 0
    def node_mutate(self):
        """A mutation type that cuts a connection between two nodes to have a third node that produces a changeable but initially indentical connection"""
        conn = random.choice(self.connections)
        new = self.new_node()
        nc1 = self.new_conn(conn.node1, new)
        nc1.weight = 1
        self.new_conn(new, conn.node2)
        self.hidden_nodes.append(new)
        conn.disable()
        return 0
    def useable_mutate(self):
        """A mutation type that disables a random connection"""
        random.choice(self.connections).disable()  # connection.invert() is also available for implementation
        return 0

    def new_node(self):
        """Wrapper for hidden node creation"""
        node = Node()
        self.hidden_nodes.append(node)
        return node
    def new_conn(self, n1, n2):
        """Wrapper for connection creation"""
        conn = Connection(n1, n2)
        self.conn_dict[conn.gene_ids] = conn
        self.connections = self.conn_dict.values()
        return conn

    def get_conn_by_id(self, id):
        """Gets a connection by inno"""
        return self.conn_dict.get(id, -1)


"""A basic node class"""
class Node:
    def __init__(self):
        self.connections = []
        self.inputs = []
        self.t_input = 0
        self.squash = ACTIVATION_FUNCTION
        self.refresh_connections()
        self.gene_id = global_innovation_number
        self.x = -1
    def refresh_connections(self):
        """Refreshes the node's inputs for use in output calculation"""
        self.inputs = list([c.get_value() for c in self.connections])
    def calculate_total_input(self):
        """Calculates the total amount of input"""
        self.refresh_connections()
        self.t_input = sum(self.inputs)
        #for c in self.connections:
        #    print(c.weight)
        #print(self.inputs)
        return self.t_input
    def output(self):
        """Gives activated output of inputs"""
        return self.squash(self.calculate_total_input())

"""Connection between two nodes"""
class Connection:
    def __init__(self, node1, node2, enabled=1, bias=1):
        global global_innovation_number
        self.node1 = node1
        self.node2 = node2
        self.gene_ids = self.node1.gene_id, self.node2.gene_id
        self.node2.connections.append(self)
        self.weight = 0
        self.enabled = enabled
        self.randomize_weight()
        self.bias = bias
    def randomize_weight(self):
        """Randomizes the connection's weight with a value -2 to 2"""
        self.weight = 1 # rand_floats(-2, 2)
        #print(self.weight)
    def enable(self):
        """Enables"""
        self.enabled = 1
    def disable(self):
        """Disables - output always multiplied by 0"""
        self.enabled = 0
    def negative(self):
        """Inverts"""
        self.enabled = -1
    def get_value(self):
        """Gets output"""
        output = self.weight * self.node1.output() * self.enabled + self.bias
        print("Output: ", output)
        return output


if __name__ == "__main__":
    pass
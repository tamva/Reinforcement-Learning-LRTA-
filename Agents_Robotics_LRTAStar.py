import random

class Node():

    def __init__(self, parent, state):
        self.parent = parent

        self.state = state

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.state == other.state

    def DelayCalculation(self):
        sum = 0
        for person in self.state:
            sum += person[2]
        return sum

def runNext_outcome(new_outcome ,world):
    new_outcome.g = new_outcome.DelayCalculation()
    new_outcome.f = new_outcome.g + new_outcome.h
    world.append_node_to_graph(new_outcome)
    return

def checkOthers(new_outcome,world):
    #f, g, and h values
    node = world.get_node_from_graph(new_outcome.state)
    node.g = new_outcome.DelayCalculation()
    node.f = new_outcome.g + node.h
    world.update_graph_node(node)

    return node

def get_min_from(open_list):
    current_node = open_list[0]
    for index, item in enumerate(open_list):
        if item.f < current_node.f:
            current_node = item

    min_elements = []
    for index, item in enumerate(open_list):
        if current_node.f == item.f:
            min_elements.append((index, item))

    random_min = random.choice(min_elements)
    return random_min[1]

def LTRA(world):

    run = True
    previous_path = []

    # Create start and end node
    starting_state = [(world.people[0], world.statelist[0], 0, 0),
         (world.people[1], world.statelist[0], 0, 0),
         (world.people[2], world.statelist[0], 0, 0),
         (world.people[3], world.statelist[0], 0, 0),
         (world.people[4], world.statelist[0], 0, 0)]

    start_node = Node(None, starting_state)
    start_node.g = start_node.h = start_node.f = 0

    # Initialize both open and closed list
    current_node = start_node

    while run:

        while world.time <= 14:

            if world.is_end_state(current_node.state):
                path = []
                current = current_node
                while current is not None:
                    # print(current.state)
                    path.append(current.state)
                    current = current.parent
                last_path = path[::-1] # Return reversed path
                break

            # Generate States
            States = []
            for move in world.next_moves(current_node.state):  # get

                new_node = Node(current_node, move)
                States.append(new_node)

            # Loop through States
            for index, new_outcome in enumerate(States):
                if world.graph_contains(new_outcome.state):
                    States[index] = checkOthers(new_outcome, world)
                else:
                    runNext_outcome(new_outcome, world)

            previous_node = current_node
            current_node = get_min_from(States)
            previous_node.h = max(previous_node.h, current_node.f)

            world.update_graph_node(previous_node)
            world.add_time()

        # check if the last path is the same with the previous one.
        # If it is the one then the Algorythm is going to finish the process
        if previous_path == last_path:
            run = False
        else:
            previous_path = last_path
            current_node = start_node
            world.time = 0

    return previous_path


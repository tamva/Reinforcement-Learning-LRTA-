from Agents_Robotics_LRTAStar import LTRA

class StateCreator:

    # the states of our problem
    statelist = [0, 1, 2, 3, 4, 5, 6, 7]
    change_state = 1
    # the 5 people of the problem
    people = [0, 1, 2, 3, 4]
    #  the transition delays for every person
    transitionDelays = [1, 0, 1, 2, 2]
    # location per half hour
    locations = [4, 6, 4, 2]


    def __init__(self, delays):

        self.start = [(0, 0, 0, 0), (1, 0, 0, 0), (2, 0, 0, 0), (3, 0, 0, 0), (4, 0, 0, 0)]#(Person, home, delay, wait)
        self.end = (2, 2, 2, 2, 2)
        self.delays = delays

        self.graph = [[] for i in range(14)]

        self.time = 0



    def add_time(self):
        self.time += 1

    def on_movie(self):
        return self.time % 2 == 0

    def avail_seats_in_cafe(self, state):
        reservedSeats = 0
        for person in state:
            if person[1] == self.statelist[4]:
                reservedSeats += 1
        return 2 - reservedSeats

    def avail_seats_in_cinema1(self, state):
        reservedSeats = 0
        for person in state:
            if person[1] == self.statelist[6]:
                reservedSeats += 1
        return 3 - reservedSeats

    def avail_seats_in_cinema2(self, state):
        reservedSeats = 0
        for person in state:
            if person[1] == self.statelist[7]:
                reservedSeats += 1
        return 3 - reservedSeats

    def checkPersons(self, agent1, agent2):
        # checks for the two agents
        if agent1 == self.people[0]:
            tmp1 = (agent1, 2, 0, self.transitionDelays[0])
        if agent1 == self.people[1]:
            tmp1 = (agent1, 4, 0, self.locations[3])
        if agent1 == self.people[2]:
            tmp1 = (agent1, 2, 0, self.transitionDelays[3])
        if agent1 == self.people[3]:
            tmp1 = (agent1, 2, 0, self.transitionDelays[4])
        if agent1 == self.people[4]:
            tmp1 = (agent1, 2, 0, self.transitionDelays[2])

        if agent2 == self.people[0]:
            tmp2 = (agent2, 2, 0, self.transitionDelays[0])
        if agent2 == self.people[1]:
            tmp2 = (agent2, 4, 0, self.locations[3])
        if agent2 == self.people[2]:
            tmp2 = (agent2, 2, 0, self.transitionDelays[3])
        if agent2 == self.people[3]:
            tmp2 = (agent2, 2, 0, self.transitionDelays[4])
        if agent2 == self.people[4]:
            tmp2 = (agent2, 2, 0, self.transitionDelays[2])
        return tmp1, tmp2

    def is_end_state(self, s):
        if s[0][1] >= 6 and s[1][1] >= 6 and s[2][1] >= 6 and s[3][1] >= 6 and s[4][1] >= 6:
            thatState = True
        else:
            thatState = False
        return thatState

    def transitions(self, person, state):

        # this part checks the location and the transitions of agents
        if person[1] == self.statelist[1]:
            if person[3] == self.change_state:
                if person[0] == self.people[1]:
                    if self.avail_seats_in_cafe(state) > 0:
                        tmp = (person[0], person[1] + 3, person[2], self.locations[3])  # Ann gets to cafe
                    else:
                        tmp = (person[0], person[1] + 2, person[2] + 1, 1)  # Ann waits to enter cafe

                if person[0] == self.people[0]:
                    tmp = (person[0], person[1] + 1, person[2], self.transitionDelays[0])  # Nick departs for cafe

                if person[0] == self.people[2]:
                    tmp = (person[0], person[1] + 1, person[2], self.transitionDelays[3])  # Tasos departs for cafe

                if person[0] == self.people[3]:
                    tmp = (person[0], person[1] + 1, person[2], self.transitionDelays[4])  # Mary departs for cafe

                if person[0] == self.people[4]:
                    tmp = (person[0], person[1] + 1, person[2], self.transitionDelays[2])  # George departs for cafe

            else:  # still have to waiting at home
                tmp = (person[0], person[1], person[2], person[3] - 1)

        elif person[1] == self.statelist[2]:
            if person[3] == self.change_state:
                if self.avail_seats_in_cafe(state) > 0:
                    tmp = (person[0], person[1] + 2, person[2], self.locations[3])
                else:  # will have to wait
                    tmp = (person[0], person[1] + 1, person[2] + 1, 1)
            else:  # still getting there
                tmp = (person[0], person[1], person[2], person[3] - 1)

        elif person[1] == self.statelist[3]:
            if self.avail_seats_in_cafe(state) > 0:
                tmp = (person[0], person[1] + 1, person[2], self.locations[3])
            else:  # will have to wait
                tmp = (person[0], person[1], person[2] + 1, 1)

        elif person[1] == self.statelist[4]:
            if person[3] == self.change_state:
                if self.time >= self.locations[0] and self.on_movie() and self.avail_seats_in_cinema1(state) > 0:
                    tmp = (person[0], person[1] + 2, person[2], self.locations[2])
                elif self.time >= self.locations[1] and self.on_movie() and self.avail_seats_in_cinema2(state) > 0:
                    tmp = (person[0], person[1] + 3, person[2], self.locations[2])
                else:  # will have to wait
                    tmp = (person[0], person[1] + 1, person[2] + 1, 1)
            else:  # still drinking coffee
                tmp = (person[0], person[1], person[2], person[3] - 1)

        elif person[1] == self.statelist[5]:
            if self.time >= self.locations[0] and self.on_movie() and self.avail_seats_in_cinema1(state) > 0:
                tmp = (person[0], person[1] + 1, person[2], self.locations[2])
            elif self.time >= self.locations[1] and self.on_movie() and self.avail_seats_in_cinema2(state) > 0:
                tmp = (person[0], person[1] + 2, person[2], self.locations[2])
            else:  # will have to wait
                tmp = (person[0], person[1], person[2] + 1, 1)

        else:
            tmp = (person[0], person[1], person[2], person[3])

        return tmp

    def remove_duplicate(self, moves):
        tmp = list(set(map(tuple, moves)))
        return tmp

    def next_moves(self, state):
        moves = []
        #in this part we check have a matrix that generates states for every agent
        if state == self.start:

            for index1, agent1 in enumerate(state):
                for index2, agent2 in enumerate(state):
                    if index2 == index1:
                        continue
                    for index3, agent3 in enumerate(state):
                        if index3 == index1 or index3 == index2:
                            continue
                        for index4, agent4 in enumerate(state):
                            if index4 == index1 or index4 == index2 or index4 == index3:
                                continue
                            for index5, agent5 in enumerate(state):
                                if index5 == index1 or index5 == index2 or index5 == index3 or index5 == index4:
                                    continue

                                for i in self.delays:
                                    for j in self.delays:
                                        for k in self.delays:
                                            tuple1, tuple2 = self.checkPersons(agent1[0], agent2[0])
                                            tuple3 = (agent3[0], 1, i//30, i//30)
                                            tuple4 = (agent4[0], 1, j//30, j//30)
                                            tuple5 = (agent5[0], 1, k//30, k//30)
                                            obj = []
                                            for h in range(5):
                                                for t in [tuple1, tuple2, tuple3, tuple4, tuple5]:
                                                    if h == t[0]:
                                                        obj.append(t)
                                            moves.append(obj)

            return self.remove_duplicate(moves)
        else:
            for person_index, person in enumerate(state):  # remove the person1 value from the person2 iteration
                moves.append(self.transitions(person, state))

            return [moves]

    def update_graph_node(self, updated_node):
        for index, node in enumerate(self.graph[self.time]):
            if node.state == updated_node.state:
                self.graph[self.time][index] = updated_node

    def append_node_to_graph(self, new_node):
        self.graph[self.time].append(new_node)

    def get_node_from_graph(self, move):
        for node in self.graph[self.time]:
            if move == node.state:
                return node

    def graph_contains(self, move):
        for node in self.graph[self.time]:
            if move == node.state:
                return True
        return False


if __name__ == "__main__":
    constant = 30
    X = StateCreator(delays=(30, 60, 90, 120, 180))
    state = LTRA(X)

    print("==================> Results <=======================")
    print("   The delays the algorithm set are the bellow")
    print("             Ann will start in {0}   ".format(state[1][1][2] * constant))
    print("             Tasos will start in {0}  ".format(state[1][2][2] * constant))
    print("             Mary will start in {0} ".format(state[1][3][2] * constant))
    print("             George will start in {0}  ".format(state[1][4][2] * constant))
    print("             Nick will start in {0}".format(state[1][0][2] * constant))
    print("====================================================")


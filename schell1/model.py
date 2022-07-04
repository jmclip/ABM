from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

# set up and initialize the agents
class SegAgent(Agent):
    def __init__(self, pos, model, agent_type):
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    # describe what happens in each step for the agents
    # agents check surroundings and count neighbors of the same type
    def step(self):
        happy = 0
        h = 0
        similar = 0
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            if neighbor.type == self.type:
                similar += 1
                #print(similar)

        # If unhappy, move:
        if similar < 8 * self.model.homophily:
            self.model.grid.move_to_empty(self)
            #print(str(similar) + " happy " + str(happy))
        else:
            self.model.happy += 1
            h = h + 1
            #print( str(h)+ ",")


    # set up the actions available to agents
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=True
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

#set up the model and initalize the world
class SegModel(Model):
    #adding agents to the world
    def __init__(self, width, height, density, minority_pc, homophily):
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily
        self.width = width
        self.height =height
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.happy = 0
        self.datacollector = DataCollector(
            {"Happy": "happy"},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as

        self.num_agents=round(density * width * height)
        #print("Expecting agents: " + str(self.num_agents))

        for i in range(self.num_agents):
            #print("this is round " + str(i))
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            if self.random.random() < self.minority_pc:
                self.agent_type = 1
            else:
                self.agent_type = 0

            #print("Round " + str(i) + " Coords " + str(x) + " and " + str(y) + " is type " + str(self.agent_type))
            agent = SegAgent(i, self, self.agent_type)
            self.schedule.add(agent)
            self.grid.position_agent(agent, (x, y))



        self.running = True #needed for batchrunner
        self.datacollector.collect(self)


    # define what happens in one step of the model
    # model stopped when all agents are happy
    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()


        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False
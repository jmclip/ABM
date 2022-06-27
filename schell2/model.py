from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import random

from mesa.batchrunner import BatchRunner

class SegAgent(Agent):
    def __init__(self, pos, model, agent_type):
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    def step(self):
        #h = 0
        similar = 0
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            if neighbor.type == self.type:
                similar += 1
                #print(similar)

        # If unhappy, move:
        if self.type == 0:
            if similar < 8 * self.model.homophily0:
                self.model.grid.move_to_empty(self)
                #print(str(similar) + " happy " + str(happy))
            else:
                self.model.happy += 1
                self.model.happy0 += 1
                #h = h + 1
                #print( str(h)+ ",")
        else:
            if similar < 8 * self.model.homophily1:
                self.model.grid.move_to_empty(self)
                #print(str(similar) + " happy " + str(happy))
            else:
                self.model.happy += 1
                self.model.happy1 += 1
                #h = h + 1
                #print( str(h)+ ",")

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=True
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

class SegModel(Model):
    #adding agents to the world
    def __init__(self, width, height, density, minority_pc, homophily0, homophily1):
        self.density = density
        self.minority_pc = minority_pc
        self.homophily0 = homophily0
        self.homophily1 = homophily1
        self.width = width
        self.height =height
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.happy = 0
        self.happy0 = 0
        self.happy1 = 0
        self.datacollector = DataCollector(
            model_reporters={"Happy": "happy",
                             "Happy Group A": "happy0",
                             "Happy Group B": "happy1"},  # Model-level count of happy agents  + subgroup counts

            # For testing purposes, agent's individual x and y
            #{"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)

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



        self.running = True
        self.datacollector.collect(self)

        # Some metrics we'll measure about our model

       # self.datacollector = DataCollector(
        #    model_reporters={"Happiness": compute_gini},
       #     agent_reporters={"Happiness": "happy"},
       # )

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.happy0 = 0  # Reset counter of happy agents
        self.happy1 = 0  # Reset counter of happy agents
        self.schedule.step()

        # collect data
        self.datacollector.collect(self)
        #happy = model.datacollector.get_model_vars_dataframe()

        if self.happy == self.schedule.get_agent_count():
            self.running = False

        # Data collection
        #schell_data = model.datacollector.get_model_vars_dataframe()
        # save the model data (stored in the pandas gini object) to CSV
       # schell_data.to_csv("model_data.csv")
        # save the agent data (stored in the pandas agent_wealth object) to CSV
        #agent_happy0_to_csv("agent_data.csv")
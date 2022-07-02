from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


# set up and initialize the agents
class SegAgent(Agent):
    def __init__(self, pos, model, agent_type):  # agents and their characteristics
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type
        self.similar = 0

    # describe what happens in each step for the agents
    # agents check surroundings and count neighbors of the same type
    def step(self):
        self.similar = 0
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            if neighbor.type == self.type:
                self.model.similar_g += 1
                self.similar +=1

                if self.type == 0:
                    self.model.similar_g0 += 1
                elif self.type == 1:
                    self.model.similar_g1 += 1


        # If unhappy, move:
        # this permits different types to have different group thresholds
        if self.type == 0:
            if self.similar < 8 * self.model.homophily0:
                self.model.grid.move_to_empty(self)
            else:
                self.model.happy += 1
                self.model.happy0 += 1
        else:
            if self.similar < 8 * self.model.homophily1:
                self.model.grid.move_to_empty(self)
            else:
                self.model.happy += 1
                self.model.happy1 += 1

    # set up the actions available to agents
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=True
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


# set up the model and initalize the world
class SegModel(Model):
    # adding agents to the world
    def __init__(self, width, height, density, minority_pc, homophily0, homophily1):
        self.density = density
        self.minority_pc = minority_pc
        self.homophily0 = homophily0
        self.homophily1 = homophily1
        self.width = width
        self.height = height
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.happy = 0
        self.happy0 = 0
        self.happy1 = 0
        self.similar_g = 0
        self.similar_g0 = 0
        self.similar_g1 = 0
        self.datacollector = DataCollector(
            model_reporters={"Pct Happy": lambda m: round(100 * m.happy / (density * width * height), 1),
                             "Pct Happy Group A": lambda m: round(100 * m.happy0 / ((1 - minority_pc) * density * width * height), 1),
                             "Pct Happy Group B": lambda m: round(100 * m.happy1 / (minority_pc * density * width * height), 1),
                             "Avg pct similar neighbors": lambda m: round(100 * m.similar_g / (8 * density * width * height), 1),
                             "Avg pct similar neighbors (A)": lambda m: round(100 * m.similar_g0 / (8 * (1 - minority_pc) * density * width * height), 1) ,
                             "Avg pct similar neighbors (B)": lambda m: round(100 * m.similar_g1 / (8 * minority_pc * density * width * height), 1)},
                              # Model-level count of happy agents  + subgroup counts
            agent_reporters={"Pct similar neighbors": lambda a: round(100 * a.similar / 8, 1),
                             "Agent type": lambda a: a.type}
                             # Agent-level reporters can allow for individual measures
        )

        # Set up agents
        self.num_agents = round(density * width * height)

        for i in range(self.num_agents):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            if self.random.random() < self.minority_pc:
                self.agent_type = 1
            else:
                self.agent_type = 0

            agent = SegAgent(i, self, self.agent_type)
            self.schedule.add(agent)
            self.grid.position_agent(agent, (x, y))

        self.running = True  # need this for batch runner
        self.datacollector.collect(self)

    # define what happens in one step of the model
    # model stopped when all agents are happy
    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.happy0 = 0  # Reset counter of happy agents
        self.happy1 = 0  # Reset counter of happy agents
        self.similar_g = 0  # Reset counter of similar agents
        self.similar_g0 = 0  # Reset counter of similar agents
        self.similar_g1 = 0  # Reset counter of similar agents
        self.schedule.step()

        if self.happy == self.schedule.get_agent_count():
            self.running = False

        # Data collection
        # extract data as a pandas Data Frame
        self.datacollector.collect(self)
        model_df = self.datacollector.get_model_vars_dataframe()
        agent_df = self.datacollector.get_agent_vars_dataframe()
        # export the data to a csv file for graphing/analysis
        model_df.to_csv("data/seg_model_gui_run_data.csv")
        agent_df.to_csv("data/seg_model_agent_gui_run_data.csv")
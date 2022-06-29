import mesa
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from model import SegModel

# calculate how many happy agents
def get_happy_agents(model):
    #Display a text count of how many happy agents there are.
   return f"Happy agents: {model.happy}"


def schelling_draw(agent):

    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.type == 0:
        portrayal["Color"] = "maroon"

    else:
        portrayal["Color"] = "mediumpurple"

    #print(agent)
    return portrayal


canvas_element = CanvasGrid(schelling_draw, 20, 20, 500, 500)
happy_chart = ChartModule([{"Label": "Happy", "Color": "Black"}])

model_params = {
    "height": 20,
    "width": 20,
    "density": UserSettableParameter('slider', "Agent density", 0.8, 0.1, 1.0, 0.1),
    "minority_pc": UserSettableParameter('slider', "Fraction minority", 0.2, 0.00, 1.0, 0.05),
    "homophily": UserSettableParameter('slider', "Homophily: (Desired % of matching neighbors) ", 0.375, 0, 1, 1/8),
}


# this is where we call the different elements we're going to be visualizing
# it includes the model, the graph/grid/world, and our various charts
# it also features a name for the model and our relevant parameter values
server = ModularServer(
    SegModel,
    [canvas_element, happy_chart],
    "Schelling's Segregation Model",
    model_params
)

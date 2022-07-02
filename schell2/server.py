import mesa
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import SegModel


# calculate how many happy agents
class HappyElement(TextElement):

    def render(self, model):
        return "% Happy agents: " + str(round(
            (model.happy / (model.density * model.width * model.height)) * 100, 1)) + "%"


class SimilarElement(TextElement):

    def render(self, model):
        similar_calc = model.similar_g / (8 * model.density * model.width * model.height) * 100
        return "Avg. % similar neighbors: " + str(round(similar_calc, 1)) + "%"


class SimilarElement0(TextElement):

    def render(self, model):
        similar_calc0 = model.similar_g0 / (
                8 * (1 - model.minority_pc) * model.density * model.width * model.height) * 100
        return "Avg. % similar neighbors (A): " + str(round(similar_calc0, 1)) + "%"


class SimilarElement1(TextElement):

    def render(self, model):
        similar_calc1 = model.similar_g1 / (8 * model.minority_pc * model.density * model.width * model.height) * 100
        return "Avg. % similar neighbors (B): " + str(round(similar_calc1, 1)) + "%"


def schelling_draw(agent):
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.type == 0:
        portrayal["Color"] = "maroon"

    else:
        portrayal["Color"] = "mediumpurple"

    return portrayal


happy_element = HappyElement()
similar_element = SimilarElement()
similar_element0 = SimilarElement0()
similar_element1 = SimilarElement1()
canvas_element = CanvasGrid(schelling_draw, 20, 20, 500, 500)
happy_chart = ChartModule([{"Label": "Pct Happy", "Color": "Black"}])
happy_chart0 = ChartModule([{"Label": "Pct Happy Group A", "Color": "Maroon"}])
happy_chart1 = ChartModule([{"Label": "Pct Happy Group B", "Color": "mediumpurple"}])

model_params = {
    "height": 20,
    "width": 20,
    "density": UserSettableParameter('slider', "Agent density", 0.8, 0.1, 1.0, 0.1),
    "minority_pc": UserSettableParameter('slider', "% group B", 0.3, 0.00, 1.0, 0.05),
    "homophily0": UserSettableParameter('slider', "Homophily Group A: (Desired % of matching neighbors) ", 0.25, 0, 1,
                                        0.125),
    "homophily1": UserSettableParameter('slider', "Homophily Group B: (Desired % of matching neighbors) ", 0.375, 0, 1,
                                        0.125),
}

# this is where we call the different elements we're going to be visualizing
# it includes the model, the graph/grid/world, and our various charts
# it also features a name for the model and our relevant parameter values
server = ModularServer(
    SegModel,
    [canvas_element, happy_element,
     similar_element, similar_element0, similar_element1,
     happy_chart,
     happy_chart0, happy_chart1],
    "Schelling's Segregation Model",
    model_params
)

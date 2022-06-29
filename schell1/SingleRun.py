from model import SegModel
from mesa.datacollection import DataCollector

model = SegModel(20, 30, 0.8, 0.2, 0.375, 0.375)
for t in range(10):
    model.step()

model_df = model.datacollector.get_model_vars_dataframe()

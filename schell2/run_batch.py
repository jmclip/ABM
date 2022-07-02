from model import SegModel
from mesa.batchrunner import FixedBatchRunner

fixed_parameters = {
    "height": 20,
    "width": 20,
    "num_agents": 350,
    "minority_pc": 0.4,
    "homophily0": 0.25,
}

parameters_list = [{"homophily1": 0.25},
                   {"homophily1": 0.375},
                   {"homophily1": 0.5}]

batch_run = FixedBatchRunner(SegModel, parameters_list,
                             fixed_parameters, iterations=10,
                             model_reporters={
                                 "Pct Happy": lambda m: round(100 * m.happy / m.num_agents, 1),
                                 "Pct Happy Group A": lambda m: round(
                                     100 * m.happy0 / m.num_agents0, 1),
                                 "Pct Happy Group B": lambda m: round(
                                     100 * m.happy1 / m.num_agents1, 1),
                                 "Avg pct similar neighbors": lambda m: m.pct_neighbors,
                                 "Avg pct similar neighbors (A)": lambda m: m.pct_neighbors0,
                                 "Avg pct similar neighbors (B)": lambda m: m.pct_neighbors1},
                             max_steps=10)

# run the batches of your model with the specified variations
batch_run.run_all()

# Data collection
# extract data as a pandas Data Frame
batch_df = batch_run.get_model_vars_dataframe()

# export the data to a csv file for graphing/analysis
batch_df.to_csv("data/seg_model_batch_run_data.csv")

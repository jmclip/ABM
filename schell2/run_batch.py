from model import SegModel
from mesa.batchrunner import FixedBatchRunner

fixed_parameters = {
    "height": 20,
    "width": 20,
    "density": 0.8,
    "minority_pc": 0.4,
    "homophily0": 0.25,
}

parameters_list = [{"homophily1": 0.25},
                   {"homophily1": 0.375},
                   {"homophily1": 0.5}]

batch_run = FixedBatchRunner(SegModel, parameters_list,
                             fixed_parameters, iterations=10,
                             model_reporters={
                                 "Pct Happy": lambda m: round(100 * m.happy / (m.density * m.width * m.height), 1),
                                 "Pct Happy Group A": lambda m: round(
                                     100 * m.happy0 / ((1 - m.minority_pc) * m.density * m.width * m.height), 1),
                                 "Pct Happy Group B": lambda m: round(
                                     100 * m.happy1 / (m.density * m.minority_pc * m.width * m.height), 1),
                                 "Avg pct similar neighbors": lambda m: round(100 * m.similar_g / (
                                         8 * m.density * m.width * m.height), 1),
                                 "Avg pct similar neighbors (A)": lambda m: round(100 * m.similar_g0 / (
                                         8 * (1 - m.minority_pc) * m.density * m.width * m.height), 1),
                                 "Avg pct similar neighbors (B)": lambda m: round(100 * m.similar_g1 / (
                                         8 * m.minority_pc * m.density * m.width * m.height), 1)
                             },
                             max_steps=1)

# run the batches of your model with the specified variations
batch_run.run_all()

# Data collection
# extract data as a pandas Data Frame
batch_df = batch_run.get_model_vars_dataframe()

# export the data to a csv file for graphing/analysis
batch_df.to_csv("data/seg_model_batch_run_data.csv")

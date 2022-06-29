from model import SegModel

#Set your parameter values for one run
# Reminder that the model takes on these parameter values:
# width, height, density, minority_pc, homophily0, homophily1

model = SegModel(20, 30, 0.8, 0.2, 2, 3)
for t in range(300):
    model.step()

#extract data as a pandas Data Frame
model_df = model.datacollector.get_model_vars_dataframe()

# export the data to a csv file for graphing/analysis
model_df.to_csv("data/seg_model_single_run_data.csv")
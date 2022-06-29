from model import SegModel
from mesa.batchrunner import FixedBatchRunner





fixed_parameters = {
    "height": 20,
    "width": 20,
    "density": 0.8,
    "minority_pc": 0.5,
    "homophily0": 2,
    #"homophily1": range(2,6) #np.arange(0.25, 0.60, 0.125)
}

parameters_list=[{"homophily1": 2},
                 {"homophily1": 3},
                 {"homophily1": 4}]



batch_run = FixedBatchRunner(SegModel, parameters_list,
                        fixed_parameters, iterations=1,
                             model_reporters={"Happy": "happy",
                                              "Happy Group A": "happy0",
                                              "Happy Group B": "happy1"}
                             )


#run the batches of your model with the specified variations
batch_run.run_all()

# Data collection
#extract data as a pandas Data Frame
#batch_df = batch_run.get_model_vars_dataframe()

# export the data to a csv file for graphing/analysis
#batch_df.to_csv("data/seg_model_batch_run_data.csv")
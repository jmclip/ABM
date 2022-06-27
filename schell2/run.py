from server import server
from model import SegModel


#model.run_model(1000)


## launch and run
#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.port = 8500
server.launch()


#model = SegModel(20, 30, 0.8, 0.2, 0.375, 0.375)
#Happy = model.datacollector.get_model_vars_dataframe()
# save the model data (stored in the pandas gini object) to CSV
#Happy.to_csv("model_data.csv")
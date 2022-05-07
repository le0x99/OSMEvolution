###  CODE : OPERATIONAL ( * TESTS PASSED) ###

from OSMEvolution.request import *
from OSMEvolution.restructure import *
import pickle
import pandas as pd

class DataCollector:
    def __init__(self, city:str):
        self.city = city
        try:
            self.area_id = get_area_id(city)
        except:
            raise Exception("There is no corresponding area ID for %s." % city)
        self.data = dict()
    def get_objects(self, object_type:str, properties:list):
        self.object_type = object_type
        self.properties = properties
        self.data["static_raw"] = get_objects(self.area_id, object_type, properties)
        self.data["static"] = pd.DataFrame(self.data["static_raw"])
        self.n_objects = len(self.data["static"])
        #return pd.DataFrame(self.data["static"])
    def build_timeseries(self, frequency:str,):
        self.data["raw_history"] = collect_history(self.data["static_raw"])
        self.data["historic_entries"] = get_entries(self.data["raw_history"])
        self.data["timeseries"] = to_df(self.data["historic_entries"], frequency)
        #return self.data["timeseries"]
    def save_data(self, name="all"):
        if name=="all":
            with open("data_dict_%s" % self.city, "wb") as f:
                pickle.dump(self.data, f)
        else:
            with open("%s_%s" % (name, self.city), "wb") as f:
                pickle.dump(self.data[name], f)

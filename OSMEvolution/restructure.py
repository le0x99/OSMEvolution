###  CODE : OPERATIONAL ( * TESTS PASSED) ###

import datetime
import pickle
from copy import deepcopy as copy
import pandas as pd
from tqdm import tqdm

def to_entries(poi_history):
    data = list()
    entries = list(poi_history.keys())
    for entry in poi_history:
        if entries.index(entry) != 0:
            prev_key = entries[entries.index(entry) - 1]
            prev_d = poi_history[prev_key]
        d = copy(poi_history[entry])
        d["entry"] = entry
        d["tag_add"] = 0
        d["tag_del"] = 0
        d["tag_change"] = 0
        d["loc_change"] = 0
        d["create"] = 0
        d["delete"] = 0
        d["modify"] = 0
        d["recreate"] = 0
        #determine action type
        if entry == 1:
            d["create"] = 1
        elif not d["visible"]:
            d["delete"] = 1
        elif not prev_d["visible"]:
            d["recreate"] = 1   
        else:
            d["modify"] = 1
            #determine modify type
            #loc change
            try:
                if any([prev_d["lat"] != d["lat"], prev_d["lon"] != d["lon"]]):
                    d["loc_change"] = 1
                    
            except:
                try:
                    if set(prev_d["nd"]) != set(d["nd"]):
                        d["loc_change"] = 1
                except:
                    d["loc_change"] = 0

            #tag add
            for tag in d["tag"]:
                if tag not in prev_d["tag"]:
                    d["tag_add"] = 1
                    break

            #tag del
            for tag in prev_d["tag"]:
                if tag not in d["tag"]:
                    d["tag_del"] = 1
                    break

            #tag change
            for tag in prev_d["tag"]:
                if tag in d["tag"] and prev_d["tag"][tag] != d["tag"][tag]:
                    d["tag_change"] = 1
                    break
        data.append(d)
        
    return data
  

    
    
# Transform poi historic edits into global city entries 
def get_entries(histories):
    data = list()
    for poi_history in tqdm(histories, desc="Extracting historic entries"):
            data += to_entries(poi_history)
    return data



# transform to dataframe with proper datetime index.
def to_df(data, freq):
    df = pd.DataFrame(data)
    df["new_mapper"] = df.index.map(lambda i : 1 if df.uid[i] not in df.uid[:i].to_list() else 0)
    df.index = df.timestamp

    df = df[['create', 'delete', 'modify', 'recreate', 'tag_add', 'tag_del', 'tag_change',
           'loc_change', "new_mapper"]]
        
    df["activity"] = df[["create", "modify", "delete", "recreate"]].sum(axis=1) 
    
    return df.resample(freq).sum()

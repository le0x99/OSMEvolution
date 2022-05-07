###  CODE : OPERATIONAL ( * TESTS PASSED) ###

import random
import time
import numpy as np
import requests
import datetime
import pickle
import pandas as pd
from copy import deepcopy as copy
from tqdm import tqdm
import osmapi
api = osmapi.OsmApi()

#get_area_id is used to generate the ID needed for the overpass.
#The official OSM IDs of the areas are not identical to the overpass area IDs, so this function generates the correct overpass ID.
#This is possible because there is a mapping between the IDs, in this case 36000000+OSMID.

def get_area_id(city:str) -> int:
    r = requests.get("https://nominatim.openstreetmap.org/search?q={}&format=json".format(city))
    data = r.json()
    for _ in data:
        if all([ _["osm_type"] == "relation",
                _["class"] == "boundary",
                _["type"] == "administrative"]):
            osm_id = _["osm_id"]
            break 
    return 3600000000 + osm_id

#The get_objects function is used to find all currently existing objects for the given area, where the type and properties of the object must be defined.
#The function (retrieve the current objects) is the only point of contact with the OverpassQueryLanguage.

def get_objects(area_id:int,
                ooi:str,
                properties:list,
                overpass_query:str=None,
                verbose:bool=False,
                return_center_location:bool=True) -> pd.DataFrame:
    init_otype = ooi
    if properties != None:
        if type(properties[0]) != list:
            for prop in properties:
                x = "[%s]" % prop
                ooi += x
            ooi = ooi + "(area.searchArea);"
        else:
            k = list()
            for props in properties:
                ooi_ = ooi
                for prop in props:
                    ooi_ += "[%s]" % prop
                k.append(ooi_)
            ooi = ""
            for f in k:
                f = f + "(area.searchArea);"
                f = f + "\n" if not k.index(f.replace("(area.searchArea);", "")) == len(k)-1 else f
                ooi += f
    overpass_url = "http://overpass-api.de/api/interpreter"
    if overpass_query == None:
        if not return_center_location:
            overpass_query = """
        [out:json][timeout:1000];
        area(%s)->.searchArea;
        (
          %s
        );
        out body;
        >;
        out skel qt;
        """ % (area_id, ooi)
        else:
            overpass_query = """
        [out:json][timeout:1000];
        area(%s)->.searchArea;
        (
          %s
        );
        out tags center;
        """ % (area_id, ooi)

    if verbose:
        print(overpass_query)
    response = requests.get(overpass_url, params = {"data" : overpass_query})
    data = response.json()
    elements = data["elements"]
    #Modify attributes
    if init_otype == "node":
        for poi in elements:
            poi["location"] = (poi["lat"], poi["lon"])
            del poi["lat"]
            del poi["lon"]
    for poi in elements:
        if "center" in poi:
            poi["lat"] = poi["center"]["lat"]
            poi["lon"] = poi["center"]["lon"]
            del poi["center"]
    return pd.DataFrame(elements)

# The function collect_history collects the historical entries of the objects.

def collect_history(pois:pd.DataFrame) -> list:
    if type(pois) == pd.DataFrame:
        pois = pois.to_dict('records')
    histories = []
    for poi in tqdm(pois, desc="Collecting historic data"):
        sleeper = random.choice([.08,.2,.12,0,.25,.01,.33])
        if poi["type"].lower() == "node":
            hist = api.NodeHistory(poi["id"])
        elif poi["type"].lower() == "way":
            hist = api.WayHistory(poi["id"])
        elif poi["type"].lower() == "relation":
            hist = api.RelationHistory(poi["id"])
        time.sleep(sleeper)
        histories.append(hist)
    return [ooi_hist for ooi_hist in histories if list(ooi_hist.keys())[0] == 1]

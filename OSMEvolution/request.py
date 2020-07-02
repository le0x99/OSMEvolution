
import osmapi
import random
import time
import requests
import datetime
from tqdm import tqdm
import pickle
from copy import deepcopy as copy
api = osmapi.OsmApi()
import pandas as pd

def get_area_id(city):
    r = requests.get("https://nominatim.openstreetmap.org/search?q={}&format=json".format(city))
    data = r.json()
    for _ in data:
        if all([ _["osm_type"] == "relation", _["class"] == "boundary", _["type"] == "administrative"]):
            osm_id = _["osm_id"]
            break 
    return 3600000000 + osm_id

def get_objects(area_id:int, ooi:str, properties:list, verbose=False):
    init_otype = ooi
    for prop in properties:
        ooi += "[%s]" % prop
    overpass_url = "http://overpass-api.de/api/interpreter"
    #["addr:street"]["addr:housenumber"]
    overpass_query = """
[out:json][timeout:1000];
area(%s)->.searchArea;
(
  %s(area.searchArea);
);
out body;
>;
out skel qt;
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
    return elements



def collect_history(pois):
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



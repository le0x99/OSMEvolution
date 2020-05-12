# OSMEvolution  🌍 📈


A package for receiving and restructuring OSM historic object data conveniently. Works for arbitrary OSM objects and all cities.


## Installation

```bash
$ pip install OSMEvolution
```

## Usage

```python3
from OSMEvolution.collect import DataCollector

# Initialize the data collector for the desired city.

>>> collector = DataCollector(city="Berlin")  
```

```python3
# Retrieve static data of the objects of interest (OOI).
# The object is defined by
      # 1. its object type (according to the OSM spatial data model).
      # 2. its object properties.
      
      
# As an example, we request the data for nodes in Berlin, whose "amenity"-key was tagged as "school".

>>> collector.get_objects(object_type="node", properties=["amenity=school"])

# The descriptive (static) data of the objects of interest can now be accessed.
# The static data is a pandas DataFrame object.

>>> static_data = collector.data.get("static").copy()
>>> static_data.head()


          id                                               tags                  location
0  237838613  {'addr:city': 'Berlin', 'addr:country': 'DE', ...  (52.4799688, 13.3384592)
1  256912446  {'addr:city': 'Berlin', 'addr:country': 'DE', ...  (52.5394411, 13.2880437)
2  256913234  {'addr:city': 'Berlin', 'addr:country': 'DE', ...   (52.521142, 13.2416342)
3  256913872  {'amenity': 'school', 'email': 'post@anna-freu...  (52.5376587, 13.2883255)
4  268915152  {'amenity': 'school', 'name': 'Klax Grundschul...  (52.5553761, 13.4307335)



# Now the historic data of the selected objects are requested, aggregated and restructured.

>>> collector.build_timeseries(frequency="m")                                                                          
Collecting historic data: 100%|████████████████████████████████████████████████████| 139/139 [00:25<00:00,  5.35it/s]
Extracting historic entries: 100%|█████████████████████████████████████████████████| 138/138 [00:00<00:00, 5708.11it/s]

# The historic data and all other data that was produced during restructuring can be acc

```



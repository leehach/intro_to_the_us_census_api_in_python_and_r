#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import pandas as pd
from pprint import pprint

HOST = "https://api.census.gov/data"
year = "2018"
dataset = "acs/acs5"
base_url = "/".join([HOST, year, dataset])

print(base_url)


# In[5]:


# Build the list of variables to request
get_vars = ["NAME", "B19013_001E"]

print(get_vars)


# In[6]:


predicates = {}
predicates["get"] = ",".join(get_vars)
predicates["for"] = "state:*"
# predicates["key"] = ____________________

print(predicates)


# In[7]:


r = requests.get(base_url, params=predicates)

print(r.url)


# In[8]:


print(r.text)


# In[9]:


# response.text is useful for diagnosing problems in the request
missing_vars = ["this_does_not_exist"]
predicates["get"] = predicates["get"] = ",".join(missing_vars)

r2 = requests.get(base_url, params=predicates)

print(r2.text)


# In[10]:


# Repair the variables...
predicates["get"] = ",".join(get_vars)

# ...but screw up the geography
predicates["for"] = "statd:*"

r2 = requests.get(base_url, params=predicates)

print(r2.text)


# In[11]:


pprint(r.json()[:5])


# In[12]:


col_names = ["name", "mhi", "state"]
states = pd.DataFrame(columns=col_names, data=r.json()[1:])

# Fix columns that should be numeric
states["mhi"] = states["mhi"].astype(int)

print(states.head())


# In[ ]:


# # Get shapefile of state boundaries
# import os
# from urllib.request import urlopen
# from zipfile import ZipFile

# # data retrieval
# def get_and_unzip(url, data_dir = os.getcwd()):
    
#     basename = url.split("/")[-1]
#     fn = os.path.join(data_dir, basename)
    
#     file_data = urlopen(url)  
#     data_to_write = file_data.read()
#     with open(fn, "wb") as f:  
#         f.write(data_to_write)
    
#     zip_obj = ZipFile(fn)
#     zip_obj.extractall(data_dir)
#     del(zip_obj)
    
#     # Cleanup:
#     os.unlink(fn)

# get_and_unzip("https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_500k.zip")


# In[13]:


import geopandas as gpd

# Rely on shapefile being downloaded and cached in R session
# Use appropriate path for yourself!
gdf = gpd.read_file("/home/lee/.cache/tigris/cb_2018_us_state_500k.shp")
gdf.plot()


# In[14]:


gdf.head()


# In[15]:


gdf.rename(columns = {"STATEFP": "state"}, inplace = True)
gdf = gdf[["state", "geometry"]]

gdf = gdf.merge(states, on = ["state"])


# In[16]:


gdf.head()


# In[22]:


# Filter to continental US and reproject
gdf = gdf[~gdf["name"].isin(["Alaska", "Hawaii", "Puerto Rico"])].copy()
gdf.to_crs(epsg = 2163, inplace = True)

gdf.plot(column = "mhi")


# In[23]:


gdf.plot(column = "mhi", cmap = "YlOrBr")


# In[24]:


# Get all the variables in a table
get_vars = ["NAME"] + ["B28010_" + str(i + 1).zfill(3) + "E" for i in range(7)]
print(get_vars)


# In[25]:


predicates = {}
predicates["get"] = ",".join(get_vars)
predicates["for"] = "county:*"
predicates["in"] = "state:42"
# predicates["key"] = ____________________

print(predicates)


# In[27]:


r = requests.get(base_url, params=predicates)

pa_counties = pd.DataFrame(columns=r.json()[0], data=r.json()[1:])

# Fix columns that should be numeric
pa_counties[pa_counties.columns[1:-2]] = pa_counties[pa_counties.columns[1:-2]].astype(int)


# In[34]:


pa_counties["pct_has_computer"] = pa_counties["B28010_002E"] / pa_counties["B28010_001E"]


# In[40]:


gdf2 = gpd.read_file("/home/lee/.cache/tigris/cb_2018_us_county_500k.shp")

gdf2.rename(columns = {"STATEFP": "state", "COUNTYFP": "county"}, inplace = True)
gdf2 = gdf2[["state", "county", "geometry"]]

gdf2 = gdf2.merge(pa_counties, on = ["state", "county"])
gdf2.to_crs(epsg = 2272, inplace = True)


# In[41]:


gdf2.head()


# In[42]:


gdf2.plot(column = "pct_has_computer", cmap = "YlGnBu")


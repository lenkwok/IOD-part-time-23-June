#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
import numpy as np
import seaborn as sns
import datetime


# In[2]:


earthquakes = pd.read_csv("/Users/lenkwok/Desktop/projects/earthquakes.csv")


# In[3]:


earthquakes.head()


# In[5]:


earthquakes['Date'].dtype


# In[26]:


earthquakes.Date=pd.to_datetime(earthquakes.Date)


# #Can't work.
# earthquakes['Date_parsed'] = pd.to_datetime(earthquakes['Date'],format="%d%m%y"

# #can't work.
# earthquakes.Date=pd.to_datetime(earthquakes.Date)

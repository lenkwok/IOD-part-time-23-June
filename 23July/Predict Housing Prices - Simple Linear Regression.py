#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Import Libraries
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt


# In[4]:


#Importing DataSet 
dataset = pd.read_csv("/Users/lenkwok/Desktop/projects/kc_house_data.csv")
space=dataset['sqft_living']
price=dataset['price']


# In[5]:


print(space)


# In[6]:


x = np.array(space).reshape(-1, 1)
y = np.array(price)


# In[7]:


#Splitting the data into Train and Test
from sklearn.model_selection import train_test_split 
xtrain, xtest, ytrain, ytest = train_test_split(x,y,test_size=1/3, random_state=0)


# In[8]:


#Fitting simple linear regression to the Training Set
from sklearn.linear_model import LinearRegression 
regressor = LinearRegression()
regressor.fit(xtrain, ytrain)


# In[9]:


#Predicting the prices
pred = regressor.predict(xtest)


# In[10]:


#Visualizing the training Test Results 
plt.scatter(xtrain, ytrain, color= 'red')
plt.plot(xtrain, regressor.predict(xtrain), color = 'blue')
plt.title ("Visuals for Training Dataset")
plt.xlabel("Space")
plt.ylabel("Price")
plt.show()


# In[11]:


#Visualizing the Test Results 
plt.scatter(xtest, ytest, color= 'red')
plt.plot(xtrain, regressor.predict(xtrain), color = 'blue')
plt.title("Visuals for Test DataSet")
plt.xlabel("Space")
plt.ylabel("Price")
plt.show()


# In[ ]:





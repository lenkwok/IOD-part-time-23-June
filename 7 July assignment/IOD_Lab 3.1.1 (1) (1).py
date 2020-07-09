#!/usr/bin/env python
# coding: utf-8

# <div>
# <img src=https://www.institutedata.com/wp-content/uploads/2019/10/iod_h_tp_primary_c.svg width="300">
# </div>

# # Lab 3.1.1 
# # *Data Wrangling and Munging with Pandas*

# ## Part 1: Wrangling Data

# The term "data wrangling" is analogous to capturing wild horses and getting them into a fenced area; the horses are data and the fencing is your computer. The more common data wrangling tasks include:
# 
# - reading flat files
# - reading Excel files
# - downloading from web pages
#   - csv
#   - html
#   - json

# In[2]:


import numpy as np
import pandas as pd


# *It is good practice to display the library version numbers for future reference:*

# In[ ]:


print('Numpy: ', np.__version__)
print('Pandas: ', pd.__version__)


# ### CSV Files

# Below are three attempts to load the file "bikeshare.csv" into a DataFrame named `bikes`. Why are they wrong?

# In[31]:


# wrong:
bikes = pd.read_table('dat/bikeshare.csv', header = None)
print(bikes.head())
print()

# wrong:
bikes = pd.read_table('dat/bikeshare.csv', header = 1)
print(bikes.head())
print()

# wrong:
bikes = pd.read_table('dat/bikeshare.csv', header = 0)
print(bikes.head())


# ?:
# ANSWER: Case 1 treats headings as just another data row. Case 2 treats the 1st data row as the column header. Case 3 gets the header right (row 0), but reads each row as a single column (Nb. the other two make that same mistake). 

# Load the file "bikeshare.csv" into a DataFrame named `bikes`, and confirm that it was loaded properly:

# In[3]:


#ANSWER:
bikes = pd.read_csv('/Users/lenkwok/Desktop/projects/bikeshare.csv')


# In[4]:


bikes.head()


# Note that we could have used `read.csv()` above. When is `read_table()` necessary?

# ?:
# ANSWER: When `sep` is not the comma character, or we need fine control that `read.csv()` does not provide.

# Flat files can be full of surprises. Here are some issues to watch out for:
# 
# - separator character is something other than the comma
#   - ";", "|", and tab are popular
# - newline character is something other than what the O/S expects 
#   - Tip: Don't hard-code the character codes for carriage returns, linefeeds, etc. Use Python's built-in representation instead (e.g. Python translates "\n" to the newline character and "\t" to the tab character on any O/S).
# - truncated lines
#   - if there are empty fields at the end of a line it is possible that their separators will be missing, resulting in a "jagged" file
# - embedded commas or quotes
#   - a free-text field containing embedded commas may split into separate fields on input
#   - a free-text field containing embedded quotes may not parse correctly
# - unescaped characters
#   - the "\" character indicates a control code to Python, which will break the I/O
#     - e.g. the substring "\u0123" will be interpreted as Unicode(0123) -- which may not be what the file creator intended
#   - these may need to be fixed by loading whole strings and then parsing into a new data frame
#   
# Tip: Most issues can be delth with by correctly specifying the parameters of the function you use to load the file. Read the doco before reading the data!

# ### Reading Excel Files

# In[11]:


from pandas import ExcelFile  # Nb. Need to install xlrd from conda (it does not automatically install with pandas)


# In[29]:


df = pd.read_excel('/Users/lenkwok/Desktop/projects/Iris.xls', sheet_name = 'Data')
df


# In[30]:


df.columns


# So, this file appears to have an embedded table of aggregates on the same sheet as the raw data (a naughty but common practice amongst analysts).

# It is usually better to load data correctly than to meddle with the source file or load it 'warts and all' and then try to parse it in code. The Pandas functions for reading files have parameters that provide the control we need. For ecxample, we could make multiple calls to `read_excel()`, using combinations of the `header`, `usecols`, `skiprows`, `nrows`, and `skipfooter` parameters to load one table at a time from a spreadsheet with multiple tables.

# Load the above file without the unwanted columns:

# In[31]:


df_col_dropped= df.drop('Species_name',axis=1)
df_col_dropped


# ### Importing Data Directly from the Web

# We usually want to store a local copy of a data file that we download from the Web, but when data retention is not a priority it is convenient to download the data directly into our running Python environment.

# #### Importing Text Files from the Web

# The web is the 'wild west' of data formats. However, we can usually expect good behaviour from files that are automatically generated by a service, such as the earthquake report:

# In[34]:


df = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_hour.csv')
df.head()


# #### Importing HTML Files from the Web
# 
# Working with unstructured HTML files relies heavily on library functions. This one, however, is well-structured:

# In[34]:


url = 'http://www.fdic.gov/bank/individual/failed/banklist.html'
df = pd.read_html(url)
df


# #### Importing XML Files from the Web
# 
# XML files are semi-structured, but you're at the mercy of the file creator. If every record has the same format it will be much easier, but practical applications often require a lot of custom code. Here is an example that includes a nice parser class: http://www.austintaylor.io/lxml/python/pandas/xml/dataframe/2016/07/08/convert-xml-to-pandas-dataframe/

# #### Importing JSON Files from the Web
# 
# Like XML, JSON files are semi-structured and may require work to capture the schema into a dataframe. Here is a simple example: 

# In[35]:


url = 'https://raw.githubusercontent.com/chrisalbon/simulated_datasets/master/data.json'

# Load the first sheet of the JSON file into a data frame
df = pd.read_json(url, orient = 'columns')
df.head()


# ## Part 2: Data Munging

# Data munging is manipulating data to get it into a form that we can start running analyses on (which usually means getting the data into a DataFrame). Before we get to this stage, we may need to remove headers or footers, transpose columns to rows, split wide data tables into long ones, and so on. (Nb. Excel files can be particularly troublesome, because users can format their data in mixed, complex shapes.) Essentially, we need to follow Hadley Wickham's guidelines for tidy datasets (http://vita.had.co.nz/papers/tidy-data.html):
# 
# The end goal of the cleaning data process:
# 
# - each variable should be in one column
# - each observation should comprise one row
# - each type of observational unit should form one table
# - include key columns for linking multiple tables
# - the top row contains (sensible) variable names
# - in general, save data as one file per table
# 

# ### Dataset Morphology

# Once we have our dataset in a DataFrame (or Series, if our data is only 1-dimensional), we can start examining its size and content.

# How many rows and columns are in `bikes`?

# In[37]:


bikes.shape


# What are the column names in `bikes`?

# In[38]:


#ANSWER
bikes.columns


# What are the data types of these columns?

# In[39]:


#ANSWER
bikes.dtypes


# What is the (row) index for this DataFrame?

# In[40]:


#ANSWER
bikes.index


# https://www.dataquest.io/blog/python-json-tutorial/

# ## Slicing and Dicing

# It is often preferable to refer to DataFrame columns by name, but there is more than one way to do this. 
# Do `bikes['season']` and `bikes[['season']]` give the same object? Demonstrate:

# In[4]:


#ANSWER
print(bikes['atemp'].head())
print(type(bikes['atemp']))
print(bikes[['atemp']].head())
print(type(bikes[['atemp']]))


# How would we use object notation to show the first 4 rows of `atemp`?

# In[6]:


#ANSWER
bikes.atemp[0:4]


# Algorithms that loop over multiple columns often access DataFrame columns by index. However, none of the following work (try them out by uncommenting / removing the "#E: " ): 

# In[ ]:


bikes[[0]]
#E: bikes[0]
#E: bikes[0,0]
#E: bikes[[0,0]]


# What is the correct way to access the 1st row of the DataFrame by its index?

# In[8]:


#ANSWER
bikes[:1]


# What is the correct way to access the 2nd column of the DataFrame by its index?

# In[15]:


#ANSWER
bikes.iloc[:,1]


# ## Handling Missing Values

# What is the Pandas `isnull` function for? 

# ?
# ANSWER:

# We can apply `isnull` to the `bikes` DataFrame to show the result for every element:

# In[16]:


bikes.isnull().head()


# However, we usually start at a higher level. How many nulls are in `bikes` altogether?

# In[18]:


#ANSWER
bikes.isnull().sum()


# If this result were nonzero we would next want to find out which columns contained nulls. How can this be done in one line of code?

# In[44]:


#ANSWER
bikes.isnull().sum()


# What is the Numpy object `nan` used for? (Write a descriptive answer.)

# ?
# ANSWER: Marking a data point as invalid.

# Write (and verify) a function that performs scalar division with built-in handling of the edge case (i.e. return a value instead of just trapping the error):

# In[ ]:


#ANSWER (need to understand how)
def divide(dividend, divisor):
    if divisor == 0:
        quotient = np.nan
    else:
        quotient = dividend / divisor
    return (quotient)

print(divide(1, 0))


# Apply the Pandas `isna` function to the following data objects:

# In[19]:


x = 2.3
y = np.nan
print(x, y)


# In[ ]:


#ANSWER
2.3 nan


# In[20]:


array = np.array([[1, np.nan, 3], [4, 5, np.nan]])
print(array)


# How is the pandas I/O parameter `na_values` used?

# ? ANSWER: writes NaN at specific locations of array

# ## Data Profiling

# ### Counts
# 
# When there are categorical variables in a dataset we will want to know how many possible values there are in each column. (Nb. If the dataset is a sample of a larger one, our sample may not capture all possible values of every categorical.)

# How many (different) seasons are in `bikes`?

# In[9]:


#ANSWER
bikes['season'].value_counts()


# ### Ranges

# Print the range of the `instant`, `dteday`, and `windspeed` columns: 

# In[11]:


#ANSWER
print('instant',bikes['instant'].min(), 'to',bikes['instant'].max())
print('dteday',bikes['dteday'].min(), 'to',bikes['dteday'].max())
print('windspeed',bikes['windspeed'].min(), 'to',bikes['windspeed'].max())


# Compute and print the overall minimum and maximum of the numeric data columns:

# In[12]:


# My answer...ah, need to filter only numeric values, leave out strings.
bikes_min, bikes_max = (min(bikes.min()), max(bikes.max()))
bikes_min, bikes_max


# In[13]:


#this is correct answer
bikes_min, bikes_max = (min(bikes.min(numeric_only=True)), 
                        max(bikes.max(numeric_only=True)))
bikes_min, bikes_max


# ### Quantiles

# Pandas makes computing quantiles easy. This is how to get the median of a Series:

# In[6]:


bikes['atemp'].quantile(0.5)


# Of course, the `quantiles` method can take a tuple as its argument. Compute the 10th, 25th, 50th, 75th, and 90th percentiles in one line of code: 

# In[7]:


#ANSWER
bikes['atemp'].quantile([0.1,0.25,0.5,0.75,0.9])


# ### Cuts
# 
# Sometimes we want to split the sample not by the quantiles of the distribution but by the range of the data. Let's take a closer look at `atemp`:

# In[8]:


type(bikes['atemp'])


# In[9]:


bikes.sample(5)


# Suppose we decide to sort these values into 4 bins of equal width, but we want to apply the resulting groups to the entire DataFrame. Basically, we need to add a row label that indcates which bin each sample belongs in. Let's call this label "atemp_level", and use the `cut` method to populate it:

# In[15]:


atemp_level = pd.cut(bikes['atemp'], bins = 4)         


# What is `atemp_level`?

# In[16]:


#ANSWER
print(type(atemp_level))


# Here is a random sample of `atemp_level`:

# In[29]:


atemp_level.sample(5)          


# So, by default, `cut` produces labels that indicate the bin boundaries for each element in the series it was applied to. Usually, we will specify labels that are appropriate to the discretisation we are applying:

# In[11]:


atemp_level = pd.cut(bikes['atemp'], bins = 4, labels = ["cool", "mild", "warm", "hot"])
atemp_level.sample(5)          


# Incorporate the new `atemp_level` column into the `bikes` DataFrame and use it to count the number of "mild" `atemp` entries in `season` 2:

# In[13]:


## Nb. could have used any column before count() in this case
bikes['atemp_level'] = atemp_level
bikes[(bikes.atemp_level == 'mild') & (bikes.season == 2)].season.count()  


# *Nb. The `atemp_level` variable we created is what the R language calls a "factor". Pandas has introduced a new data type called "category" that is similar to R's factors.*

# # Synthetic Data
# 
# Sometimes we may want to generate test data, or we may need to initalise a series, matrix, or data frame for input to an algorithm. Numpy has several methods we can use for this.

# Execute the following, then check the shape and content of each variable:

# In[14]:


# Creating arrays with initial values
a = np.zeros((3))
b = np.ones((1,3))
c = np.random.randint(1,10,(2,3,4))   # randint(low, high, size)
d = np.arange(4)
e = np.array( [[1,2,3,4], [5,6,7,8]] )


# In[ ]:


# Cleaning Data


# ## Load Data
# 
# Load rock.csv and clean the dataset.

# In[15]:


#Load csv file
rock=pd.read_csv('/Users/lenkwok/Desktop/projects/rock.csv')


# ## Check Column Names
# 
# Check column names and clean.

# In[48]:


rock.columns


# In[ ]:


#Columns names are not uniform.
# Use clean_column_names(x, gate = "dummy", object = "Main")
#Arguments
x 	 a data frame

Gate 	 gate name to be cleared, given as a regular expression; defaults to "dummy", which does nothing, unless there is a gate called "dummy"

object	name of object to be cleared; defaults to "Main"


    Uppercase, Lowercase > Lowercase
    Space > _
    get_ipython().run_line_magic('pinfo', '')


# In[17]:


def clean_column_name(column_names):
    clean_column_names = []
    for c in column_names:
        c = c.lower().replace(' ', '_')
        c = c.lower().replace('*', '')
        c = c.lower().replace('?', '')
        clean_column_names.append(c)
        
    return clean_column_names


# In[18]:


rock.columns = clean_column_name(rock.columns)


# # Replace Null Values With 0
# 
# Check 'release' column whether this column have any null value or not. Replace null value with 0.

# In[49]:


rock.isnull().sum()


# In[20]:


#Masks are an array of boolean values for which a condition is met.  
## Create a mask to find all rows with null values
null_mask = rock['release_year'].isnull()
print(null_mask)


# In[22]:


#Use mask to extract NaN values
print(rock[null_mask])


# In[24]:


# or we can use loc to locate using labels
rock.loc[null_mask, 'release_year'] = 0
rock


# In[25]:


# Check is there any nul values in any column
rock.isnull().sum()


# # Check Datatypes of Dataset
# 
# Check datatypes of the dataset. Is there any column which should be int instead of object? Fix the column. 

# In[51]:


rock.info()


# In[52]:


# Check values of release_year, which shouldn't be object.  
# 577 entries for release year have NaN
rock['release_year'].value_counts()


# In[51]:


# Convert release year to numeric.   Songfacts.com is not valid release year
rock['release_year'] = pd.to_numeric(rock['release_year'])


# In[53]:


# Create a mask to find all rows with SONGFACTS.COM and make them NaN
rock.loc[song_facts_mask, 'release_year'] = 'SONGFACTS.COM'
rock.loc[song_facts_mask, 'release_year'] = np.NaN


# In[55]:


# Let's try again to convert release year to numeric
rock['release_year'] = pd.to_numeric(rock['release_year'])


# In[56]:


# Check data types.  Ah, this time release year is finally float!
rock.dtypes


# # Check Min, Max of Each Column
# 
# Is there any illogical value in any column? How can we fix that?

# In[48]:


def check_min_max(rock):
    # Check min, max of each column
    print(rock.describe().['min', 'max']
    


# In[49]:


def check_min_max(df):
    # Check min, max of each column
    print(df.describe().T[['min', 'max']])


# In[50]:


check_min_max(rock)


# # Write Some Functions

# ## Write a function that will take a row of a DataFrame and print out the song, artist, and whether or not the release date is < 1970

# In[57]:


rock.dtypes


# In[31]:


def check_song(row):
    print('Song: ', row['song_clean'])
    print('Artist: ', row['artist_clean'])
    print('Released before 1970: ', row['release_year'] < 1970)
    print('\n')


# In[58]:


# Check any row using index, say row 2
check_song(rock.iloc[1])


# In[59]:


# Check first five rows
rock.head()


# ## Write a function that converts cells in a DataFrame to float and otherwise replaces them with np.nan

# In[60]:


def convert_to_float(column):
    column = pd.to_numeric(column, errors='coerce')
    return column


# ## Apply these functions to your dataset

# In[61]:


rock.apply(convert_to_float)


# ## Describe the new float-only DataFrame.

# In[62]:


rock.describe()


# In[63]:


#Transpose
rock.describe().T


# In[ ]:





# >
# 

# >
# 

# >
# 

# 
# 
# ---
# 
# 
# 
# ---
# 
# 
# 
# > > > > > > > > > © 2019 Institute of Data
# 
# 
# ---
# 
# 
# 
# ---
# 
# 
# 
# 

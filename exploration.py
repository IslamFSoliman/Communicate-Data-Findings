#!/usr/bin/env python
# coding: utf-8

# # FordGoBike Data Exploration
# ## by Islam Soliman
# 
# 
# ### Table of Content
# - [Introduction](#intro)
# - [Preliminary Wrangling](#preliminary)
#     - [Loading Libraries](#loading)
#     - [Gathering Data](#gathering)
#     - [Assessing Data](#assessing)
#     - [Cleaning Data](#cleaning)
#     - [Storing Data](#storing)
# - [Exploratory Data Analysis](#exploratory)
#     - [Univariate Exploration](#univariate)
#     - [Bivariate Exploration](#bivariate)
#     - [Multivariate Exploration](#multivariate)
# - [Explanatory Data Analysis](#explanatory)
# - [Summary](#summary)
# - [References](#references)
# 
# 
# ****
# 
# <a id='intro'></a>
# ## Introduction
# 
# Ford GoBike is the San Francisco Bay Area's bike share system. The Bike Share was introduced in 2013 as a pilot program for the region, with 700 bikes covering 70 stations across San Francisco and San Jose. It is now called **Baywheels**.
# 
# Baywheels, like other bike share systems, consists of a fleet of specially designed, sturdy and durable bikes that are locked into a network of docking stations throughout the city. The bikes can be unlocked from one station and returned to any other station in the system, making them ideal for one-way trips. People use bike share to commute to work or school, run errands, get to appointments or social engagements and more. It's a fun, convenient and affordable way to get around.
# 
# The bikes are available for use 24/7 all year round, and riders have access to all bikes in the network when they become a member or purchase a pass.
# 
# 
# ****
# 
# <a id='preliminary'></a>
# ## Preliminary Wrangling
# 
# The dataset was downloaded from [here](https://s3.amazonaws.com/baywheels-data/index.html) for `February and March 2020`, I will be joining the data files together creating a single dataset that would require data wrangling to get it ready for the analysis.

# <a id='loading'></a>
# ## Loading Libraries

# In[1]:


# import all packages and set plots to be embedded inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import datetime
import zipfile
import requests
import io

get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='gathering'></a>
# ## Gathering Data

# In[2]:


def fetch_csv(month, year = 2020):
    '''
    This function takes two inputs (month and year) "though I made the year constant since I won't change it later"
    , uses request to get the required zip file, unzip the file, read the included CSV file
    , and finally, save the same in a datafile.
    '''
    re = requests.get(f'https://s3.amazonaws.com/baywheels-data/{year}{month}-baywheels-tripdata.csv.zip')
    zip_file = zipfile.ZipFile(io.BytesIO(re.content))
    csv_file = zip_file.open(f'{year}{month}-baywheels-tripdata.csv')
    
    df = pd.read_csv(csv_file)
    df.to_csv(f'data{month}-{year}.csv',index=False)


# In[3]:


# Fetching and reading February 2020 datafile
fetch_csv('02')
# Mitigating the low_memory error by specifying Column(13) dtype
df1 = pd.read_csv('data02-2020.csv', dtype={'rental_access_method': object})
# Display the top five rows from the loaded data file
df1.head()


# In[4]:


# Fetching and reading March 2020 datafile
fetch_csv('03')
df2 = pd.read_csv('data03-2020.csv')
# Display the top five rows from the loaded data file
df2.head()


# ****

# <a id='assessing'></a>
# ## Assessing Data

# ### Starting with February 2020 data assessment

# In[5]:


# Getting the basic dataframe information, dtypes and shape
df1.info()
df1.shape


# In[6]:


# Sampling the data to get a feel for the data, and understand the required cleaning
df1.sample(10)


# In[7]:


# Checking the dataframe's basic statistical information
df1.describe()


# In[8]:


# Checking 10 trips with the shortest duration
df1.nsmallest(10, ['duration_sec'])


# In[9]:


# Checking how many trips with the shortest recorded duration '60sec'
df1[df1.duration_sec == 60].count()


# In[10]:


# Checking 10 trips with the longest duration
df1.nlargest(10, ['duration_sec'])


# In[11]:


# Checking any duplicated reecords
df1.duplicated().sum()


# In[12]:


# Checking any NaN values
df1.isna().sum()
# It looks like some of the starting and ending values are NaN


# In[13]:


df1.user_type.value_counts()


# In[14]:


df1.rental_access_method.value_counts()


# ### Continuing with March 2020 data assessment

# In[15]:


# Getting the basic dataframe information, dtypes and shape
df2.info()
df2.shape


# In[16]:


# Sampling the data to get a feel for the data, and understand the required cleaning
df2.sample(10)


# In[17]:


# Checking the dataframe's basic statistical information
df2.describe()


# In[18]:


# Checking 10 trips with the shortest duration
df2.nsmallest(10, ['duration_sec'])


# In[19]:


# Checking how many trips with the shortest recorded duration '60sec'
df2[df2.duration_sec == 60].count()


# In[20]:


# Checking 10 trips with the longest duration
df2.nlargest(10, ['duration_sec'])


# In[21]:


# Checking any duplicated reecords
df1.duplicated().sum()


# In[22]:


# Checking any NaN values
df1.isna().sum()
# It looks like some of the starting and ending values are NaN


# In[23]:


df1.user_type.value_counts()


# In[24]:


df1.rental_access_method.value_counts()


# ## Findings
# ### Tidiness Findings
#     T1 "Month" column is missing in both dataframes.
#     T2 Data is divided into two separate dataframes.
#     T3 "Day" column with day name is missing in both dataframes.
#     T4 Starting and Ending hour columns are missing in both dataframes.
#     T5 Duration in seconds only delivers unclear perception of time.
#     T6 There are several columns that are not required for the analysis.
# ### Quality Findings
#     Q1 Wrong datatypes ('start_time', 'end_time', 'start_station_id', 'end_station_id', ETC..)
#     Q2 Missing data records

# ****

# <a id='cleaning'></a>
# ## Cleaning Data
# ### Creating Copies from the Dataframes

# In[25]:


wrangled_df1 = df1.copy()
wrangled_df2 = df2.copy()


# ****
# ### Cleaning Tidiness Findings
# ### T1 "Month" column is missing in both dataframes.
# ### Define:
# Adding a month column to both dataframes with the month name as value for easy identification.
# ### Code:

# In[26]:


wrangled_df1['month'] = 'february'
wrangled_df2['month'] = 'march'


# In[27]:


# Storing dataframes into CSV files excluding index column
wrangled_df1.to_csv('wrangled_feb.csv', index=False)
wrangled_df1.to_csv('baywheels_2020.csv', index=False) # This will be the main data file.
wrangled_df2.to_csv('wrangled_mar.csv', index=False)


# ### Testing:

# In[28]:


wrangled_df1 = pd.read_csv('wrangled_feb.csv', dtype={'rental_access_method': object})
wrangled_df1.head()
wrangled_df1.shape


# In[29]:


wrangled_df2 = pd.read_csv('wrangled_mar.csv')
wrangled_df2.head()
wrangled_df2.shape


# ****
# ### T2 Data is divided into two separate dataframes.
# ### Define:
# Append (wrangled_mar.csv) file to (baywheels_2020.csv) excluding the header row.
# ### Code:

# In[30]:


main_df = pd.read_csv('baywheels_2020.csv', dtype={'rental_access_method': object})
main_df = main_df.append(pd.read_csv('wrangled_mar.csv'))


# ### Testing:

# In[31]:


main_df.info()
main_df.shape


# #### Merging data into (baywheels_2020.csv) successful with the total rows in both dataframes

# ****
# ### T3 "Day" column with day name is missing in both dataframes.
# ### Define:
# Adding two more columns containing (start_day, end_day) obtained from (start_time, end_time) columns after converting the dtypes to datetime
# ### Code:

# In[32]:


# Converting both 'start_time', 'end_time' dtype to datetime.
main_df[['start_time', 'end_time']] = main_df[['start_time', 'end_time']].apply(pd.to_datetime)


# In[33]:


# Creating 'start_day', 'end_day' columns.
main_df.insert(3, 'start_day', main_df['start_time'].dt.day_name())
main_df.insert(4, 'end_day', main_df['end_time'].dt.day_name())


# ### Testing:

# In[34]:


main_df.info()
main_df.shape


# ****
# ### T4 Starting and Ending hour columns are missing in both dataframes.
# ### Define:
# Adding two more columns containing (start_hour, end_hour) obtained from (start_time, end_time) to use during my Univariate Exploration.
# ### Code:

# In[35]:


main_df.insert(5, 'start_hour', main_df['start_time'].dt.hour)
main_df.insert(6, 'end_hour', main_df['end_time'].dt.hour)


# ### Testing

# In[36]:


main_df.info()
main_df.shape


# ****
# ### T5 Duration in seconds only delivers unclear perception of time.
# ### Define:
# Adding Minutes, Hours, and Days columns for trip duration.
# ### Code:

# In[37]:


main_df.insert(1, 'duration_min', main_df.duration_sec/60)
main_df.insert(2, 'duration_hrs', main_df.duration_sec/3600)
main_df.insert(3, 'duration_days', main_df.duration_hrs/24)


# In[38]:


main_df['duration_min'] = main_df['duration_min'].astype(int)
main_df['duration_hrs'] = main_df['duration_hrs'].astype(int)


# ### Testing:

# In[39]:


main_df.head()


# ****
# ### T6 There are several columns that are not required for the analysis.
# ### Define:
# Delete unrequired columns ('start_station_latitude', 'start_station_longitude', 'end_station_latitude', 'end_station_longitude')
# ### Code:

# In[40]:


main_df.drop(['start_station_latitude', 'start_station_longitude', 'end_station_latitude', 'end_station_longitude'], axis=1, inplace=True)


# ### Testing:

# In[41]:


main_df.info()
main_df.shape


# ****

# ## Cleaning Quality Findings
# ### Q1 Wrong datatypes ('start_time', 'end_time', 'start_station_id', 'end_station_id', ETC..)
# ### Define
# Converting 'start_station_id', 'end_station_id', 'bike_id' to string since there won't have any operations performed on them, and 'user_type', 'rental_access_method' to category.
# <br>**Note:** start_time, end_time had been converted to datetime at T3.
# ### Code:

# In[42]:


main_df[['start_station_id', 'end_station_id', 'bike_id']] = main_df[['start_station_id', 'end_station_id', 'bike_id']].astype(str)
main_df[['user_type', 'rental_access_method']] = main_df[['user_type', 'rental_access_method']].astype('category')


# ### Testing:

# In[43]:


main_df.info()


# ****

# <a id='storing'></a>
# ## Storing Data

# In[44]:


main_df.to_csv('wrangled_baywheels_2020.csv', index=False)


# ### What is the structure of your dataset?
# 
# > The data is straightforward to understand. This data has been collected efficiently, providing a valuable collection of data to work with and draw conclusions from.
# <br><br>This notebook uses data collected from February and March 2020. There are approximately 609,153 bike rides.
# <br><br>The column header descriptions are as follows (each trip is anonymized):<br>
# ><ul>
#   <li>Trip Duration (seconds)
#   <ul>
#   <li>Start Time and Date
#   <li>End Time and Date
#   </ul>
#   <li>Start Station ID
#   <ul>    
#   <li>Start Station Name
#   <li>Start Station Latitude
#   <li>Start Station Longitude
#   </ul>
#   <li>End Station ID
#   <ul>
#   <li>End Station Name
#   <li>End Station Latitude
#   <li>End Station Longitude
#   </ul>
#   <li>Bike ID
#   <li>User Type (Subscriber or Customer – “Subscriber” = Member or “Customer” = Casual)
#   <li>Rental Method (App or Clipper)
#  </ul>     
# <br>I added the following columns in my cleaning efforts:<br>
# ><ul>
#   <li>Trip Duration (Minutes)
#   <li>Trip Duration (Hours)
#   <li>Trip Duration (Days)
#   <li>Start Day of the Week
#   <li>End Day of the Week
#   <li>ٍStart Hour
#   <li>End Hour
#   <li>Month
#  </ul>
# 
# ### What is/are the main feature(s) of interest in your dataset?
# 
# > The main features of interests in the data are the start and end time of a ride. This can be used to find out when bikes are in high or low demand. There is also data related to the users of the service whether they are a paying member or a casual user. These features can be used to make business decisions such as which day of the week bikes are mostly available and if there is any increament in bikes numbers is required.
# 
# ### What features in the dataset do you think will help support your investigation into your feature(s) of interest?
# 
# > The start and end times, and related time-based information will be utilized heavily. I will also use the customer related data to understand the user-driven data behind each ride.
# ****

# <a id='exploratory'></a>
# ## Exploratory Data Analysis

# <a id='univariate'></a>
# ## Univariate Exploration

# In[45]:


wrangled_df = pd.read_csv('wrangled_baywheels_2020.csv', dtype={'rental_access_method': object})
wrangled_df.head()


# In[46]:


wrangled_df.describe()


# In[47]:


base_color = sb.color_palette()[0] # Removing the colours and setting to the variable base_color
sb.set_style("darkgrid")


# In[48]:


# Usage of Baywheels system during Weekday
plt.figure(figsize=[15, 8])
weekday = wrangled_df['start_day'].value_counts(ascending=True).index # Reversing the current order
sb.countplot(data = wrangled_df, y = 'start_day', color = base_color, order = weekday)
plt.title('Baywheels Usage by Weekday', y=1.05, fontsize=16, fontweight='bold')
plt.ylabel('Weekdays', fontsize=14, fontweight='bold')
plt.xlabel('Number of Bike Trips', fontsize=14, fontweight='bold')
plt.xticks(rotation=45);


# #### Maximum trips were started on `Wednesday`.

# In[49]:


# Usage of Baywheels system during Weekday
plt.figure(figsize=[15, 8])
weekday = wrangled_df['end_day'].value_counts(ascending=True).index # Reversing the current order
sb.countplot(data = wrangled_df, y = 'end_day', color = base_color, order = weekday)
plt.title('Baywheels Trips Ending Daily', y=1.05, fontsize=16, fontweight='bold')
plt.ylabel('Weekdays', fontsize=14, fontweight='bold')
plt.xlabel('Number of Bike Trips', fontsize=14, fontweight='bold')
plt.xticks(rotation=45);


# #### Maximum trips were ended on `Wednesday`.

# In[50]:


wrangled_df.start_day.value_counts()


# In[51]:


wrangled_df.end_day.value_counts()


# **Observation 1:** `Wednesdays and Tuesdays` seem to be the most popular days for using the baywheels system, however `Thursdays, Mondays and Fridays` are very close in numbers.<br>The usage drops significantly on `Saturdays and Sundays` indicating the baywheels system is used primarily for commuting purposes during working days.
# ****

# In[52]:


# Checking the duration of trips in SECONDS
plt.figure(figsize=[15, 8])
bin_edges = np.arange(0, 3600, 60) # Adjusting the axis to clearly see most data points.

plt.hist(data = wrangled_df, x = 'duration_sec', bins = bin_edges, rwidth = 0.8,  color = base_color);
plt.title("Baywheels System Trip Duration in Seconds", y=1.05, fontsize=16, fontweight='bold')
plt.xlabel('Duration in Seconds', fontsize=12, fontweight='bold')
plt.ylabel('Number of Bike Trips', fontsize=12, fontweight='bold')
plt.xticks(rotation=45);


# In[53]:


# Checking the duration of trips in minutes
plt.figure(figsize=[15, 8])
bin_edges = np.arange(0, 45, 1) 
ticks = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
lables = ['{}'.format(val) for val in ticks]

plt.hist(data = wrangled_df, x = 'duration_min', bins = bin_edges, rwidth = 0.8,  color = base_color)
plt.title('Baywheels System Trip Duration in Minutes', y=1.05, fontsize=16, fontweight='bold')
plt.xlabel('Duration in Minutes', fontsize=12, fontweight='bold')
plt.ylabel('Number of Bike Trips', fontsize=12, fontweight='bold')
plt.xticks(ticks, lables);


# In[54]:


wrangled_df.duration_min.describe()


# **Observation 2:** The `average trip` is just under `13.5 minutes`, with `75%` of trips being under `15 minutes`. Looking at the histogram, most rides fall in between the `3 - 13 minute range`.<br>This suggests riders are using the bikes for short distances.
# ****

# In[55]:


plt.figure(figsize=[15, 8])
sb.countplot(data = wrangled_df, x = 'start_hour', color = base_color)
plt.title('Baywheels System Usage per Hour', y=1.05, fontsize=16, fontweight='bold')
plt.xlabel('Hours', fontsize=14, fontweight='bold')
plt.ylabel('Number of Bike Trips', fontsize=14, fontweight='bold');


# **Observation 3:** The bikes saw the most usage during the `morning` hours of `8 - 9am`, and in the `afternoon` hours of `4 - 6pm`, which is a typical workday.<br>This furthers the suggestion that the bikes are being used primarily for commuters.
# ****

# ### Discuss the distribution(s) of your variable(s) of interest. Were there any unusual points? Did you need to perform any transformations?
# 
# > Due to thorough data cleaning efforts there were no big surprises during the exploratory analysis and visualization phase.<br>There is no need for transformations to provide good insights.
# 
# ### Of the features you investigated, were there any unusual distributions? Did you perform any operations on the data to tidy, adjust, or change the form of the data? If so, why did you do this?
# 
# > Nothing seems out of the ordinary for a bike sharing system in a major city. So far, the data reveals that the primary use for the system falls during working days mainly for daily commutes.
# 
# ****

# <a id='bivariate'></a>
# ## Bivariate Exploration
# 
# > In this section, investigate relationships between pairs of variables in your
# data. Make sure the variables that you cover here have been introduced in some
# fashion in the previous section (univariate exploration).

# In[56]:


# Customers vs Subscribers
plt.figure(figsize = [15, 10])
labls = wrangled_df["user_type"].value_counts().index
explode = (0.1, 0)

plt.pie(wrangled_df["user_type"].value_counts(), explode=explode, labels=labls, autopct='%1.1f%%', shadow=True, startangle=90)
plt.title('Baywheels System - Customers Vs Subscribers', y=1.05, fontsize=16, fontweight='bold')
plt.axis('equal')
plt.show()


# In[57]:


# Customers vs Subscribers Usage per Hour
plt.figure(figsize=[15, 8])
sb.countplot(data = wrangled_df, x = "user_type", order = wrangled_df.user_type.value_counts().index)
plt.title('Baywheels System Usage per Hour', y=1.05, fontsize=16, fontweight='bold')
plt.xlabel('User Type', fontsize=14, fontweight='bold')
plt.ylabel('Number of Bike Trips', fontsize=14, fontweight='bold');


# In[58]:


wrangled_df.user_type.value_counts()


# **Observation 1:** The majority of users of the Baywheels Bike System are `Subscribers 61.3%` i.e. customers who subscribe to the monthly membership. While `customers` who pays by trip are `38.7%`.
# ****

# In[59]:


# Customer Usage by Weekday vs. Subscriber Usage by Weekday
plt.figure(figsize=(15, 8))

wrangled_df_user_week = wrangled_df.groupby(['start_day', 'user_type']).size().reset_index()
weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

ax = sb.pointplot(data=wrangled_df_user_week, x='start_day', y=0, hue = 'user_type', scale=.7, order = weekday);

plt.title('Baywheels System Daily Utilization by User Type', y=1.05, fontsize=16, fontweight='bold')
plt.xlabel('Weekdays', fontsize=14, fontweight='bold')
plt.ylabel('Number of Bike Trips', fontsize=14, fontweight='bold')
plt.xticks(rotation=45);
plt.grid()


# **Observation 2:** The point plot above is an excellent visual showing the *sharp contrast* between `Customers and Subscribers`.
# <br>`Customers` have a relatively *`low usage`* of the Baywheels system with a sharp decline on the weekends.
# <br>`Subscribers` are the opposite, there is a steadily *`high usage`* on weekdays, with a minute increase on the weekend.
# ****

# In[60]:


# Customer Usage by Duration vs. Subscriber Usage by Duration

plt.figure(figsize=(15, 8))
data = wrangled_df.query('duration_min <= 60')

sb.violinplot(data=data, x='user_type', y='duration_min', color = base_color)

plt.title('Baywheels System - Customers vs. Subscribers Ride Duration in Minutes', y=1.05, fontsize=16, fontweight='bold')
plt.xlabel('User Type', fontsize=14, fontweight='bold')
plt.ylabel('Duration in Minutes', fontsize=14, fontweight='bold');


# **Observation 3:** The plots above show the ride duration spread in minutes.
# <br>Both `customers and subscribers` have used the Bike sharing system almost *`equal`* in duration, less than or equal to 60 minutes.
# ****

# ### Talk about some of the relationships you observed in this part of the investigation. How did the feature(s) of interest vary with other features in the dataset?
# 
# > Adding the user type to the analysis revealed different behavior usage between **`customers and subscribers`**. The data suggests that **customers** are *`casual riders`* such as tourists, or students on a school vacation or holiday.
# <br>This is accurate when factoring in that **`Customer`** usage increases on the weekends.
# <br>In contrast, the data suggests **Subscribers** are *`daily commuters`* or full time students who use the system during weekdays, better weather, and mostly for shorter distances. They mainly rent bikes before and after a typical work or school day `(8-9am and 4-6pm)`.
# 
# ### Did you observe any interesting relationships between the other features (not the main feature(s) of interest)?
# 
# > There is almost no difference in the trip duration between **`customers and subscribers`**.
# <br>**Customers** trips are slightly longer than for subscribers, most probably due to the fact they prefer bike rides around weekends in summertime, which may be for longer trips around the surrounding area.
# <br>**Subscribers** uses the system mainly for commuting purposes so they prefer quick, short rides to and from work.
# 
# ****

# <a id='multivariate'></a>
# ## Multivariate Exploration
# 
# > Create plots of three or more variables to investigate your data even
# further. Make sure that your investigations are justified, and follow from
# your work in the previous sections.

# In[61]:


# Plotting hours, day type, user type, and average duration
g = sb.relplot(
    kind="line", data=wrangled_df, x="start_hour", y="duration_min", 
    estimator=np.mean, hue="user_type", col="start_day", 
    height=4, aspect=1, col_wrap=4,
)

(g.set_axis_labels("Hour of Day", "Trip Duration (Min)")
  .set_titles("Weeday: {col_name}")
  .tight_layout(w_pad=0));


# ### Talk about some of the relationships you observed in this part of the investigation. Were there features that strengthened each other in terms of looking at your feature(s) of interest?
# 
# > This section essentially amplified the previous data topics of exploration by adding in more variables to compare with other variables, each user group uses the bike sharing system.<br>As previously noted, Customers use the system at almost the same time as the Subscribers.
# 
# ### Were there any interesting or surprising interactions between features?
# 
# > Nothing out of the expected here. It was interesting to note the sharp difference for customer vs. subscribers vs. Trip Duration during the mornign hours the begining of the Week (Monday). This may be a potential loss of possible Customers converting to Subscribers.

# ***
# ### Summary
# This project is a *win - win situation* where the company and a large number of people can benefit from this program:
# 
# - **Subscribers** `61.3%` (i.e. daily commuters) benefit from a healthy commuting choice.
# - **Customers** `38.7%` (i.e. tourists, students, etc.) have a sustainable, yet flexible option for touring the city.
# - The use of the service peaks mainly at `08:00AM` and `05:00PM`. This is due to work and school times in the United States.
# - **Weekdays** shows *`more demand`* for the service, while **weekends** witness the *`lowest utilisation`* of service.
# - The majority of **trip duration** falls between *`20 minutes or less`*.
# - The busiest day of week is **Monday**.
# - The **average** subscriber **trip duration** is about *`10 minutes`* and it seems to be fixed within that range without major fluctuations.
# - The **variation** for *`customers`* tends to be more that that of *`subscribers`*.
# ***

# ### Sources
# - [Data Files](https://s3.amazonaws.com/baywheels-data/index.html)
# - [Kimberly Fessel - YouTube](https://www.youtube.com/channel/UCirb0k3PnuQnRjh8tTJHJuA)
# - [Corey Schafer - YouTube](https://www.youtube.com/c/Coreyms)
# - [Matplotlib Official Cheat Sheets](https://matplotlib.org/cheatsheets/)
# - [Seaborn Official Documentation](https://seaborn.pydata.org/index.html)
# - [Pandas for Everyone](https://www.amazon.com/Pandas-Everyone-Analysis-Addison-Wesley-Analytics-ebook/dp/B0789WKTKJ/ref=pd_sim_2/141-0065686-7219252?pd_rd_w=g9ByO&pf_rd_p=6caf1c3a-a843-4189-8efc-81b67e85dc96&pf_rd_r=CF17Y9MQYSH3JF49KJVZ&pd_rd_r=712655ce-1880-4f4c-8d98-46fb45fe7dd9&pd_rd_wg=5IlzT&pd_rd_i=B0789WKTKJ&psc=1)
# - [Hands On Data Analysis with Pandas](https://www.amazon.com/Hands-Data-Analysis-Pandas-visualization-ebook/dp/B07KJQN1CC/ref=pd_sim_3/141-0065686-7219252?pd_rd_w=g9ByO&pf_rd_p=6caf1c3a-a843-4189-8efc-81b67e85dc96&pf_rd_r=CF17Y9MQYSH3JF49KJVZ&pd_rd_r=712655ce-1880-4f4c-8d98-46fb45fe7dd9&pd_rd_wg=5IlzT&pd_rd_i=B07KJQN1CC&psc=1)

# In[63]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'exploration.ipynb'])


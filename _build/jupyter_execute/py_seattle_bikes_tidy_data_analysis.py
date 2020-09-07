# Introduction to Data Wrangling using pydatatable

# 1. Objective

**This notebook would  teach yours how to get started doing your data analysis in Pydatatable way. It’s seamlessly process your higher volumes of data in a faster manner unlike other python data handling libraries. to get along with it you have to be comfortable with SQL querying, basic python programming and basic mathematics.** 

# 2. Introduction to pydatatable

**Pydatatable is an extremely fast and memory efficient package for transforming data in python, which is similar to R data.table package. It's silent features are** 

1. Concise syntax: fast to type, fast to read
2. Fast speed
3. Memory efficient
4. Careful API lifecycle management
5. Support from H2O's team and growing community
6. Open sourced project

**Note:** Refer H2O's pydatatable documentation for more info

# 3. Exploratory Data Analysis on Seattle Bike traffic data

* I'm going to use **Tidy Tuesday(R4DS Online learning community)'s** project data - Seattle Bike traffic for this notebook, here they do release an interesting dataset weekly once to get our hands dirty with it and enhance our EDA Skills.

## 3.1 Setup libraries 

* It's an easy step to download datatable into python environment and it can be installed from **PyPi** pip as showed in below chunk.

# Install datatable package
!pip install datatable

* Once datatable is successfully installed it can be loaded into our environment by calling it via import statements as described in below chunk, along with **datatable** few of other packages(pandas,numpy,seaborn and matplotlib) are required to be loaded for this analysis 

# Loading libraries
import datatable as dt
from datatable import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import altair as alt
sns.set_style('whitegrid')
plt.style.use('ggplot')
#plt.style.use('fivethirtyeight')

* We should first check what version of datatable is being used and we are going to make use of the recent version of datatable for this analysis

print(f'The loaded datable version is : {dt.__version__}')

## 3.2 Importing data

1. A file will be loaded and stored into our environment in the form of rows and columns for further analysis by calling a function  **fread** from dt, and it supports various file (csv/xlsx/txt/jay etc.. etc...) formats.
2. We can load data from our local system or from any spcific web resource
3. We can also create datatables manually by calling a function **Frame** 
4. Pandas dataframe can be converted to a datatable frame
5. Datatable can also be changed to Pandas dataframe (vice versa) and these cases/techniques will be discussed as our analysis go further

# Importing data
seattle_bikes_dt = dt.fread("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-04-02/bike_traffic.csv")

## 3.3 Introduction to data and basic data manipulations in pydatatable

##### Notes: 
1. Seattle bike data has been downloaded via web resource and created a datatable frame with a name **seattle_bikes_dt**
2. Now we would like to perform data operations such as adding/removing/modifying observations or fields,grouping/reshaping/joining frames,and carrying out caluclations on observations. 
3. The standard syntax for getting the above mentioned things done is showed in the below attached image

4. **i** is a row selector, **j** is a  column selector  addional parameters such as **by/sort/join **
5. Take data.table dt,subset rows using **i** and manipulate columns with **j**, grouped according to by or ordered or sorted observations.
6. Datatable index Slicing in i and j will be as same as pandas/numpy/generic python index slicing principles 


* Here is our first data operation on DT is that looking at first five observation i.e from 0:5(excluded) is given in i followed by a comma(,), and after that the symbol(:) should be put in if we want to select all DT coulmns.
* If we would like to select only few columns J should be filled in with index slicing or column names in the f-expression sytax style(avail only in Pydatatable), it will be covered in next steps


# Glance at first 5 observations
seattle_bikes_dt[0:5,:]

* By default Datatable frame prints the first 10 and last 5 observation when it's called, here these can be be changed as per our requirement by setting the options of display head/tail rows as follows. 

# Setting dt row configuration to display first 4 and last 4 observations
dt.options.display.head_nrows=4
dt.options.display.tail_nrows=4
##dt.options.display.max_nrows=8

* Now lets print a seattle bike datatable and it will show only first 4 and last 4 observations

# looking at first 4 and last 4observations
seattle_bikes_dt

##### Notes:
1. Here are couple of interim reasons to convert a Datatable DT to pandas DF
2. Pydatatable is still in an initial development stages for data manipulations, few of python visual libraries aren't supporting Frame object yet, so to overcome this, DT needs to be in a form of pandas DF when a visulization is required in any EDA for time being. but in future Datatable Frame support for visualizations specially in Seaborn/Matplotlib would be made available 
3. Reshaping of DT frames are yet to be introduced in DT
4. Few of Date and String objects operations are not yet implemented in DT
5. In the coming days, DT will hopefully  bring in all functionalities/features required for doing data manipulation without needing these DT to DF conversions(vice-versa)  

##### Notes: 
* Our seattle bike DT has a column **date** in string object, here if it is modified to a date object we can extract few more fields(year,day,month,weekday etc..etc..) from it for our analysis.
* So,we are now going to learn how to convert DT - seatle_bikes_dt to a pandas DF, here DT Frame has a function called **to_pandas()**, with the help of this function the required convertion can be achieved as below. Here remember that the converted pandas DF should always be assigned to a new pandas object with a name.

# Creating a pandas df from dt
seattle_bikes_df = seattle_bikes_dt.to_pandas()

* Seattle bike pandas dataframe columns info can be checked here.

# Look at pandas seatle bike df col names and types
seattle_bikes_df.info()


* The below code chunks will guide us how the date columns are organized/manipulated.?

# changing date column type in seatle df
seattle_bikes_df['date']= pd.to_datetime(seattle_bikes_df['date'],format="%m/%d/%Y %I:%M:%S %p")

# Glance at seatle df field types
seattle_bikes_df.info()

# A df with Additional columns created from date type  
seatle_dates_df = pd.DataFrame({
    
    'year' : seattle_bikes_df['date'].dt.year,
    'month': seattle_bikes_df['date'].dt.month,
    'day'  : seattle_bikes_df['date'].dt.day,
    'hour' : seattle_bikes_df['date'].dt.hour,
    'week_day': seattle_bikes_df['date'].dt.day_name()
    
})

##### Notes:
* Now have a pandas DF **seattle_dates_df** with these columns- year,month,day,hour and week_day, and it needs to be converted to a DT for further analysis
* Here, a DF should be passed to **dt.Frame()** method and assigned to a new DT with name as illustrated below

# Convering date df to dt
seatle_dates_dt = dt.Frame(seatle_dates_df)

* In our original seattle DT we no more require date column in string format, so better to remove it from DT  

# delating a string date column from dt
del seattle_bikes_dt['date']

* The DT's seattle_dates_dt and seattle_bikes_dt will be concatenated with the help of **dt.cbind()** function

# Concatinating two dts to have a tidy dt
seatle_bikes_dt_tidy = dt.cbind(seatle_dates_dt,seattle_bikes_dt)

# Tidy DT first 4 and last 4 observations
seatle_bikes_dt_tidy

##### Notes:
* We can see that a column crossing has a different categorical level values, and 3 of them are having longer names, to make them shorter their values should be updated/modified with shorter string values. 
* In Datatable it can be achived as done in below 4 code chunks.
* here is a simple syntax for this: DT[column value condition, the column to be updated]='new value'

# Modifying observations of crossing col - set - 1
seatle_bikes_dt_tidy[f.crossing=="39th Ave NE Greenway at NE 62nd St",f.crossing]='Greenwayway-NE-62Strt'

# Modifying observations of crossing col - set - 2
seatle_bikes_dt_tidy[f.crossing=="Broadway Cycle Track North Of E Union St",f.crossing]='BroadwayCycleTrack-N'

# Modifying observations of crossing col - set - 3
seatle_bikes_dt_tidy[f.crossing=="NW 58th St Greenway at 22nd Ave",f.crossing]='Greenway-NW-58Strt'

* We have a tidied DT version of seattle DT, and lets see what are the column names and their type's.

# Checking field types of dt
for i in range(0,seatle_bikes_dt_tidy.shape[1]):
    print(f'The column - {seatle_bikes_dt_tidy.names[i]} - is a type of {seatle_bikes_dt_tidy.stypes[i]}')

##### Notes:
* We have seen that a column **ped_count** has a type - int, it's original values are 0 and 1, so they were treated as Integers. but we require them to be a bool
* Its type needs to be casted to a bool type 
* Syntax to do it: DT['colname to be casted'] = new dt type

# Converting pedestrian column value to a type bool
seatle_bikes_dt_tidy['ped_count']=dt.bool8

##### Notes:

* Seattle DT has a column ped_count with numeric and NA values,
* we should use this function dt.isna(col_name_to_be_checked) to check a DT column has any NA value
* This symbol can be useful ~ as a negation to it i.e ~dt.isna(col)
* We are going to filter observations whose ped_count is not NA's in the below chunk

# Viewing observations whose ped_count is not NA's
seatle_bikes_dt_tidy[~dt.isna(f.ped_count),:]

### Part-B

## EDA Questions:

1. How many of bikes/pedestrains have passed though the different crossings?
2. How many of bikes/pedestrains have gone from the direction?
3. How many of bikes/pedestrians have passed though crossings from different directions?
4. How have been Seattle - Bike traffic trends over the years?
5. When in the day(Hours) do people bike through these Seattle crossings ?
6. When in the day(Time Intervals)  do people bike through these Seattle crossings ?
7. When in days do people bike through these Seattle crossings ?
8. When in months? do people bike through these Seattle crossings ? 
9. In which directions do people commute by bike?



### 3 . EDA - 1 : How many of bikes/pedestrains have passed though the different crossings?

# Data manipulation and Visualization
alt.Chart(seatle_bikes_dt_tidy[:,count(),by(f.crossing)
                                     ][:,:,sort(-f.count)
                                      ].to_pandas()).mark_bar().encode(
    alt.X('count'),alt.Y('crossing',sort='-x')).properties(
    title='Bike/ped passed throgh crossings')

##### EDA-1 DT Syntax explanation:
1. grouped on crossing to count how many of bikes/ped passed,chained by a sort on count to have a higher to lower counts order for visualization 
2. DT[:,i,:by] -- i should be with (:) to consider all the observation, in i count() function should be given in, and in by a column should be given in a datatable f-expression style i.e f.crossing
3. a chain [] needs be applied to DT do sorting on a field count and it will help us to have a ordered values
4. DT has to be converted to a pandas DF as we are going to do a visualization on the resulted DT.
5. As said earlier Seaborn/matplotlibs are not yet supporting Datatable Frame object

### 3 . EDA - 2 : How many of bikes/pedestrains have gone from the direction?

# Data vis and Manipulation
alt.Chart(seatle_bikes_dt_tidy[:,count(),by(f.direction)
                                     ][:,:,sort(-f.count)
                                      ].to_pandas()
         ).mark_bar().encode(alt.X('count'),alt.Y('direction',sort='-x')).properties(title='Bikes/ped passed from directions')

##### EDA - 2 Syntax explanation

1. It's manipulation sytax is as same as to EDA -1


### 3 . EDA- 3: How many of bikes/pedestrians have passed though crossings from different directions?

# Data Vis
alt.Chart(seatle_bikes_dt_tidy[:,{
                'total': count()
            },by(f.direction,f.crossing)
            ].to_pandas()).mark_bar().encode(
    alt.Y('crossing',sort='-x'),alt.X('total'),alt.Color('direction')).properties(title='Bikes/Ped crossing from different directions')

##### EDA - 3 Syntax explanation

Grouping performed on two fields: direction and crossing specified in f-expression, their counts gets assigned to a variable named total, and it's temporarily created for our reference purpose or further manipulation if it was to be continued      

### 3. EDA - 4 : How have been Seattle - Bike traffic trends over the years?

# Data Vis
alt.Chart(seatle_bikes_dt_tidy[:,count(),by(f.year)].to_pandas()).mark_line().encode(alt.X('year:N'),alt.Y('count'))

##### EDA - 4 Syntax explanation

Same as above ones

# Groupig based on NA's field
seatle_bikes_dt_tidy[:,{
    'total':count()
},by(dt.isna(f.ped_count),
     f.year,f.crossing)
]

##### EDA - 4.1 Syntax explanation

dt.isna is a function to check an observation is a Null or Not, here how many of ped_count NA's per year and crossing were caluclated  

### 3. EDA - 5: When in the day(Hours) do people bike through these Seattle crossings ?

alt.Chart(seatle_bikes_dt_tidy[:,{'bike_count':dt.sum(f.bike_count)},by(f.crossing,f.hour)
                    ][:,{'hour':f.hour,
                         'pct_bike' : dt.math.rint((f.bike_count/dt.sum(f.bike_count))*100)
                        },by(f.crossing)
                     ].to_pandas()).mark_line().encode(
    alt.X('hour:N'),alt.Y('pct_bike'),alt.Color('crossing',legend=None)).properties(
    width=280,height=160).facet(
    facet='crossing',
    columns=4)

##### EDA - 5 Syntax explanation

In first chain of DT: grouping has been done on crossing and hour fields so that the total bike count was summed and assigned to a variable-bike_count and in second chain, grouping applied only on crossing to caluclate the percent of bike crossed each direction and an hour. here **dt.math** is a module provides mathematical functions.

# Glance at data
seatle_bikes_dt_tidy

# Taking hours col value
horas = seatle_bikes_dt_tidy[:,f.hour]

* Hour field contains values from 0 to 23, I would like to constuct an another field binning these hours into 4 different time windows.
* Hour field only selected from seatle_bikes_tidy and assigned it to a new DT horas
* Hours binning done as showed in below code chunk, and it will be available in List form
* The list of time windows will be turned into a DT called time_window_dt

# Binning on Horas DT column
horas_bins = ["Morning" if (dia>=7 and dia <11) else
 "Mid Day" if (dia>=11 and dia <16) else
 "Evening" if (dia>=16 and dia <18) else "Night" for dia in horas['hour'].to_list()[0]]

# Framing a new DT from the above list of time bins
time_window_dt=dt.Frame(time_window=horas_bins)

* dt.cbind is a function to append/concatenate two datatable columns
* DT's: time_window and horas have beeen concatenated

# Concatinating two DT's
time_window_hour_dt = dt.cbind(horas,time_window_dt)

* Hour and time_windows unique values extracted as follows, dt.first is a function that will give us a first observation of a DT like head gives first five.

# Creating Unique hours
time_window_hour_dt_unique_dict = time_window_hour_dt[:,first(f[1:]),by(f[0])]

* We have a unique value DT, and key needs to be assigned to a hour field for doing DT join operations further. Remember that key columns won't permit duplicate values 

# Setting a key index on dt for joining 
time_window_hour_dt_unique_dict.key="hour"

* dt.join used to perform joinings on DT's, pydatatables join operations are much faster and a key must be exist on a DT which is going to be joined.
* Time window DT is going to be joined to seattle bikes DT as showed below. 

# A new DT created after joining the 2 DT's using inner join
seatle_bikes_dt_tidy_v_1 = seatle_bikes_dt_tidy[:,:,join(time_window_hour_dt_unique_dict)]

# Check how many of time windows are existed in joined dt
seatle_bikes_dt_tidy_v_1[:,count(),by(f.time_window)]

# a new DT- bikes pass through crossings
seatle_bikes_per_crossing_dt = seatle_bikes_dt_tidy_v_1[:,{
    'missing_bike_counts':dt.sum(dt.isna(f.bike_count)),
    'bike_counts':dt.sum(f.bike_count)
    },by(f.crossing,f.time_window)
][:,{
    'time_window': f.time_window,
    'missing_bike_counts':f.missing_bike_counts,
    'bike_counts' : f.bike_counts,
    'bike_percent_cross' : dt.math.rint((f.bike_counts/dt.sum(f.bike_counts))*100)      
},by(f.crossing)]

##### EDA - 6 Syntax explanation

In first chain of DT: grouping has been done on crossing and timw window fields so that the total bike count was summed and assigned to a variable - bike_count, another new variable also created to tell how many of missing values existed in bike_count field and in second chain, grouping applied only on crossing to caluclate the percent of bike crossed each direction and an hour. here **dt.math** is a module provides mathematical functions

# Top two observation of bike cross rates in each of crossings
seatle_bikes_per_crossing_dt[:2,:,by(f.crossing),sort(-f.bike_percent_cross)]

* grouped by crossing, sorted on bike_percent_cross in descending order and display first two observations only i.e :2, if we want 10 then it will be as :10. 

# Least two observation of bike cross rates in each of crossings
seatle_bikes_per_crossing_dt[:2,:,by(f.crossing),sort(f.bike_percent_cross)]

* grouped by crossing, sorted on bike_percent_cross in ascending order and display first two observations only i.e :2, if we want 10 then it will be as :10. 

# A first observation per each crossing
seatle_bikes_per_crossing_dt[:,first(f[1:]),by(f.crossing)]

# A last observation per each crossing
seatle_bikes_per_crossing_dt[:,last(f[1:]),by(f.crossing)]

### 3 . EDA - 6 : When in the day(Time Intervals)  do people bike through these Seattle crossings?

# Visualization
alt.Chart(seatle_bikes_per_crossing_dt.to_pandas()).mark_bar().encode(alt.X('bike_percent_cross'),alt.Y('time_window',sort='-x'))

alt.Chart(seatle_bikes_per_crossing_dt.to_pandas()).mark_bar().encode(
    alt.Y('time_window',sort='-x'),alt.X('bike_percent_cross'),alt.Color('crossing',legend=None)
).properties(width=220,height=180).facet(facet='crossing',columns=4)

# Data aggregations
seatle_bikes_per_crossing_days_dt = seatle_bikes_dt_tidy_v_1[:,{
    'missing_bike_counts':dt.sum(dt.isna(f.bike_count)),
    'bike_counts':dt.sum(f.bike_count)
    },by(f.crossing,f.week_day,f.hour)
][:,{
    'week_day': f.week_day,
    'missing_bike_counts':f.missing_bike_counts,
    'bike_counts' : f.bike_counts,
    'bike_percent_cross' : (f.bike_counts/dt.sum(f.bike_counts))*100     
},by(f.crossing)]

# glance at DT
seatle_bikes_per_crossing_days_dt

### 3. EDA - 7 : When in days do people bike through these Seattle crossings ?

alt.Chart(seatle_bikes_per_crossing_days_dt.to_pandas()).mark_bar().encode(
    alt.Y('week_day'),alt.X('bike_percent_cross')
).properties(width=220,height=180).facet(facet='crossing',columns=4)

### 3. EDA - 8 : When in months? do people bike through these Seattle crossings ?

# Creating a DT
seatle_bikes_per_crossing_months_dt = seatle_bikes_dt_tidy_v_1[:,{
    'missing_bike_counts':dt.sum(dt.isna(f.bike_count)),
    'bike_counts':dt.sum(f.bike_count)
    },by(f.crossing,f.month)
][:,{
    'month': f.month,
    'missing_bike_counts':f.missing_bike_counts,
    'bike_counts' : f.bike_counts,
    'bike_percent_cross' : (f.bike_counts/dt.sum(f.bike_counts))*100     
},by(f.crossing)]

# Changing a month field type to string
seatle_bikes_per_crossing_months_dt['month'] = str32

alt.Chart(seatle_bikes_per_crossing_months_dt.to_pandas()).mark_bar().encode(
    alt.Y('month:N'),alt.X('bike_percent_cross'),alt.Color('crossing',legend=None)
).properties(width=220,height=180).facet(facet='crossing',columns=4)

### 3. EDA - 9 : In which directions do people commute by bike?

# Creating a DT
seatle_bikes_per_crossing_day_hour_dt = seatle_bikes_dt_tidy_v_1[:,{
    'missing_bike_counts':dt.sum(dt.isna(f.bike_count)),
    'bike_counts':dt.sum(f.bike_count)
    },by(f.crossing,f.week_day,f.hour)
][:,{
    'week_day': f.week_day,
    'hour' : f.hour,
    'missing_bike_counts':f.missing_bike_counts,
    'bike_counts' : f.bike_counts,
    'bike_percent_cross' : (f.bike_counts/dt.sum(f.bike_counts))*100     
},by(f.crossing)]

# Glance
seatle_bikes_per_crossing_day_hour_dt

alt.Chart(seatle_bikes_per_crossing_day_hour_dt.to_pandas()).mark_bar().encode(
    alt.X('hour:N'),alt.Y('bike_percent_cross'),alt.Color('week_day',legend=None)
).properties(width=280,height=160).facet(facet='week_day',columns=4)

# 4. References and Recommendations

1. Pydatatable documentation : [https://datatable.readthedocs.io/en/latest/index.html](http://)

2. Post your doubts/questions on Stackoverflow with these tags [python]+[datatable], and datatable team and community members will reach yours out with their answers/suggestions.

3. There are couple of introductory tutorials on Kaggle written by SRK, ParulPandey so on..

4. There is a talk at pydata-LA,[https://www.youtube.com/watch?v=CmGez-LPR_0&t=248s](http://) by H2O's team
5. If you would like to open any issues or contribute for pydatatable development you can approach here on github: [https://github.com/h2oai/datatable](http://)
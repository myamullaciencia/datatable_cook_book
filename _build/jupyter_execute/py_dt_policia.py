# Py: Tidy data analysis - Police traffic activity 

We are going to make use of data from a open source project https://openpolicing.stanford.edu/ and we have collected data belongs to the state: Rhode Island for this analysis.

# Importing libraries
import datatable as dt
import pandas as pd
import altair as alt
from datatable import f,by,count,update,sort,join

# Datatable options are set to display limit number of rows and datatable frame columns colors are maintained
dt.init_styles()
dt.options.display.head_nrows=4
dt.options.display.tail_nrows=4

# Importing data of police activities
policia_dt = dt.fread('https://assets.datacamp.com/production/repositories/1497/datasets/62bd9feef451860db02d26553613a299721882e8/police.csv',na_strings=[""])

# Importing weather reports for the state RI
weather_dt = dt.fread('https://assets.datacamp.com/production/repositories/1497/datasets/02f3fb2d4416d3f6626e1117688e0386784e8e55/weather.csv',na_strings=[""])

# Glance
policia_dt

# Glance
weather_dt

weather_dt = weather_dt[:,([f.DATE,f.TAVG,f.TMIN,f.TMAX])]

weather_dt.names = {'DATE': "stop_date",
                    'TAVG': "temp_avg",
                    'TMIN': "temp_min",
                    'TMAX': "temp_max"}

weather_dt

weather_dt.key="stop_date"

# count the number of missing values
policia_dt.countna()

del policia_dt[:,['county_name', 'state']]

# glance
policia_dt

policia_dt[:,count(),by(f.driver_gender)]

policia_tidy_dt = policia_dt[~dt.isna(f.driver_gender),:]

policia_tidy_dt[:,count(),by(f.violation)
               ][:,f[:].extend({'grand_tot':dt.sum(f.count)})
                ][:,f[:].extend({'prop':f.count/f.grand_tot})
                 ][:,f[:].remove(f.grand_tot),sort(-f.prop)
                  ]

# custom function to generate a summary report per a single group column
def py_dt_one_group_proportions_summary(DT,por):
    
    DT_summary = DT[:,dt.count(),by(f[por])
                   ][:,f[:].extend({'grand_tot':dt.sum(f.count)})
                    ][:,f[:].extend({'prop':f.count/f.grand_tot})
                     ][:,f[:].remove(f.grand_tot),dt.sort(-f.prop)
                      ]
    return DT_summary

py_dt_one_group_proportions_summary(policia_tidy_dt,'search_conducted')

policia_tidy_dt[:,count(),by(f.driver_gender,f.violation)
               ][:,f[:].extend({'group_tot':dt.sum(f.count)}),by(f.driver_gender)
                ][:,f[:].extend({'prop':f.count/f.group_tot})
                 ][:,f[:].remove(f[1])]

# custom function to generate a summary report per two groups column
def py_dt_two_group_proportions_summary(DT,por1,por2):
    
    DT_summary = DT[:,dt.count(),by(f[por1],f[por2])
                   ][:,f[:].extend({'group_tot':dt.sum(f.count)}),by(f[por1])
                    ][:,f[:].extend({'prop':f.count/f.group_tot})
                     ][:,f[:].remove(f[1])
                      ]
    
    return DT_summary

py_dt_two_group_proportions_summary(policia_tidy_dt[f.violation=="Speeding",:],'driver_gender','stop_outcome')

py_dt_one_group_proportions_summary(policia_tidy_dt,'search_conducted')

py_dt_two_group_proportions_summary(policia_tidy_dt,'driver_gender','search_conducted')

py_dt_one_group_proportions_summary(policia_tidy_dt,'search_type')[~dt.isna(f.search_type),:]

policia_tidy_dt[dt.f.search_type.re_match("[\w\s\W]+Frisk"),:
               ][:,count(),by(f.driver_gender)]

py_dt_one_group_proportions_summary(policia_tidy_dt,'stop_duration')

py_dt_two_group_proportions_summary(policia_tidy_dt,'stop_duration','is_arrested')

py_dt_two_group_proportions_summary(policia_tidy_dt,'driver_race','is_arrested')

# stop time
stop_time_df = policia_tidy_dt[:,(f.stop_time)].to_pandas()

# extracting hour
stop_time_hour = stop_time_df.stop_time.str.extract(r'([\d]{2})')

# a new dataframe
stop_time_hour_dt = dt.Frame(stop_time_hour)

# change a col name
stop_time_hour_dt.names={'0':'stop_hour'}

# Binding two dts
policia_tidy_dt_v1 = dt.cbind(policia_tidy_dt,stop_time_hour_dt)

# Hour wise arrests
hour_wise_arrests_dt = py_dt_two_group_proportions_summary(policia_tidy_dt_v1,'stop_hour','is_arrested')

# Visualization
alt.Chart(hour_wise_arrests_dt.to_pandas()).mark_bar().encode(
    alt.X('stop_hour:N'),
    alt.Y('count'),
    alt.Color('is_arrested')
).properties(

    title= 'Hour wise arrest trends'
)

# Hour wise arrest rates
hour_wise_arrests_rates_dt= hour_wise_arrests_dt[f.is_arrested==True,:
                                                ][:,dt.mean(f.count),by(f.stop_hour)
                                                 ]

# Visualization
alt.Chart(hour_wise_arrests_rates_dt.to_pandas()).mark_line().encode(
    alt.X('stop_hour'),
    alt.Y('count')
).properties(

    title = 'Hourly wise - average arrest rates'
)

py_dt_one_group_proportions_summary(policia_tidy_dt_v1,'drugs_related_stop')

# stop date and converting to pandas frame
stop_date_df = policia_tidy_dt[:,(f.stop_date)].to_pandas()

# converting to date object
stop_date_df = stop_date_df.apply(lambda x: pd.to_datetime(x,format="%Y-%m-%d"))

# extracting year and months
stop_year_month_dt = dt.cbind(dt.Frame({'year':list(stop_date_df['stop_date'].dt.year)}),
                              dt.Frame({'month':list(stop_date_df['stop_date'].dt.month)})
                             )

# Joining two DTs
policia_tidy_dt_v2 = dt.cbind(policia_tidy_dt_v1,stop_year_month_dt
                             )[:,f[:].remove([f[0],f[1]])]

# Year wise counts drug related stops
policia_tidy_dt_v2[f.drugs_related_stop==True,:
                  ][:,count(),by(f.year)
                   ]

# Joining police and weather dataframes
policia_tidy_dt_v3 = policia_dt[:,:,join(weather_dt)]

weather_dt

# Visualization
alt.Chart(weather_dt.to_pandas()).transform_fold(
    
    ['temp_avg','temp_min','temp_max'],
    as_=['temp_type','temp_val']
    
).mark_boxplot().encode(
    
    alt.Y('temp_type:O'),
    alt.X('temp_val:Q')
    
).properties(title='Weather temp distributions')

# Adding a new column temp_diff
weather_dt[:,update(temp_diff=f.temp_max-f.temp_min)]

# Visualiztion
alt.Chart(weather_dt[:,f.temp_diff].to_pandas()).mark_bar().encode(
    alt.X('temp_diff',bin=True),
    alt.Y('count()')
).properties(

    title='Distribution of temparature differences'
)

# Downloading weather data and selecting specific columns related to weather conditions
weather_temp = dt.fread('https://assets.datacamp.com/production/repositories/1497/datasets/02f3fb2d4416d3f6626e1117688e0386784e8e55/weather.csv',na_strings=[""]
                       )[:,[f[1],f[7:]]]

weather_temp

# New column : sum of rows
weather_temp[:,update(tot_cond=dt.rowsum(f[1:]))]

# select few columms
weather_temp_1= weather_temp[:,[f[0],f[-1]]]

# renaming dataframe column
weather_temp_1.names = {'DATE':'stop_date'}

# apply a key
weather_temp_1.key="stop_date"

# Visualization
alt.Chart(weather_temp_1.to_pandas()).mark_bar().encode(
    alt.X('tot_cond',bin=True),
    alt.Y('count()')
).properties(
    title='Weather conditions distribution'
)

# Joining two dataframes
policia_tidy_dt_v4 = policia_tidy_dt_v3[:,:,join(weather_temp_1)]

# selecting first 5 and last 4 columns
policia_tidy_dt_v4[:,[f[:5],f[-4:]]]

# Speed violation 
policia_zone_speed_violations_weather = py_dt_two_group_proportions_summary(policia_tidy_dt_v4[f.violation=="Speeding",:],'district','tot_cond')

# Visualization
alt.Chart(policia_zone_speed_violations_weather.to_pandas()).mark_bar().encode(
    alt.Y('district'),
    alt.X('count'),
    alt.Color('tot_cond')
).properties(

    title='Speed Violations - Disticts and weather conditions'
)


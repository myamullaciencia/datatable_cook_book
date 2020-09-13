# Py: Tidy data analysis - Friends

Friends is an American television sitcom, created by David Crane and Marta Kauffman, which aired on NBC from September 22, 1994, to May 6, 2004, lasting ten seasons. With an ensemble cast starring Jennifer Aniston, Courteney Cox, Lisa Kudrow, Matt LeBlanc, Matthew Perry and David Schwimmer, the show revolves around six friends in their 20s and 30s who live in Manhattan, New York City. The series was produced by Bright/Kauffman/Crane Productions, in association with Warner Bros. Television. The original executive producers were Kevin S. Bright, Kauffman, and Crane.

# Importing libraries
import datatable as dt
import pandas as pd
import altair as alt
from datatable import f,by,count,update,sort,join
import re

dt.options.display.head_nrows=4
dt.options.display.tail_nrows=4
dt.init_styles()

# Importign data
amigos_info_dt = dt.fread('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-09-08/friends_info.csv')
amigos_dt = dt.fread('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-09-08/friends.csv')

# Glance
amigos_info_dt

# Seasons
amigos_info_dt[:,count(),by(f.season)]

# Unique episodes per a season
amigos_info_dt[:,count(),by(f.season,f.episode)
              ][:,{'unique_episodes':count()},by(f.season)
               ]

# average views and ratings per season
amigos_info_dt[:,dt.mean(f[-2:]),by(f.season)]

# Highest rating title
amigos_info_dt[f.imdb_rating==dt.max(f.imdb_rating),:]

# lowest rating title
amigos_info_dt[f.imdb_rating==dt.min(f.imdb_rating),:]

# Top 2 titles having higher rating per season
amigos_info_dt[:2,:,by(f.season),sort(-f.imdb_rating)]

# find a title info
amigos_info_dt[f.title=="The Last One",:]

# select few observations till 235
amigos_info_dt[[slice(None,235)],:]

alt.Chart(amigos_info_dt[:,[f.season,f.episode,f.us_views_millions]].to_pandas()).mark_point().encode(
    alt.X('episode'),
    alt.Y('us_views_millions')
).properties(
    title=' Episode and views'
)

# Average views and rating per directors
directors_views_rating = amigos_info_dt[:,dt.mean(f[-2:]),by(f.directed_by)
                                       ][:,:,dt.sort(-f.imdb_rating)
                                        ]

# Top 10 directors who have made more titles
directors_dt = amigos_info_dt[:,count(),by(f.directed_by)
                             ][:10,:,dt.sort(-f.count)
                              ]

# setting a key on DT
directors_dt.key='directed_by'

# First 5 and last 5 observations
directors_views_rating[[slice(5),slice(25,None)],:]

# directors and their avg title rating and total titles
directors_views_rating_v1 = directors_views_rating[:,:,dt.join(directors_dt)
                                                  ][~dt.isna(f.count),:
                                                   ][:,:,dt.sort(-f.count)
                                                    ]

directors_views_rating_v1

alt.Chart(directors_views_rating_v1.to_pandas()).mark_bar().encode(
    alt.Y('directed_by',sort='-x'),
    alt.X('count'),
    alt.Color('imdb_rating')
).properties(
    
    title='Top directors title counts and imdb ratings'
)

alt.Chart(directors_views_rating_v1.to_pandas()).mark_bar().encode(
    alt.Y('directed_by',sort='-x'),
    alt.X('count'),
    alt.Color('us_views_millions')
).properties(
    
    title='Top directors title counts and US million views'
)

# are the directors and writers same for a title ?
amigos_info_dt[:,dt.update(temp=f.directed_by==f.written_by)]

# are the directors and writers same for a title ?
amigos_info_dt[f.temp==True,:]

# remove the temp col
del amigos_info_dt["temp"]

# split writers column
writers_list = [ elemento.split('&') for elemento in amigos_info_dt[:,f.written_by].to_list()[0] ]

# create a new DT with writers
writers_dt = dt.Frame({'no_of_writers':[len(elem) for elem in writers_list]})

# Joining two DTs
amigos_info_dt_v1 = dt.cbind(amigos_info_dt,writers_dt)

# No of writers 
alt.Chart(amigos_info_dt_v1[:,count(),by(f.no_of_writers)].to_pandas()).mark_bar().encode(

    alt.X('count'),
    alt.Y('no_of_writers:O')
).properties(
    
    title='Number of writers in titles'
)

amigos_year = dt.Frame({'year':[re.findall(r'[\d]{4}',fecha)[0] for fecha in amigos_info_dt_v1[:,f.air_date].to_list()[0] ]})

alt.Chart(amigos_year[:,count(),by(f.year)].to_pandas()).mark_line().encode(alt.X('year'),alt.Y('count'))

amigos_dt

amigos_info_df = amigos_info_dt.to_pandas()

amigos_df = amigos_dt.to_pandas()

amigos_todo_dt = dt.Frame( amigos_info_df.join(amigos_df.set_index(['season','episode']),
                                               on=['season','episode']) 
                         )

amigos_todo_dt

amigos_todo_dt[~dt.isna(f.speaker),:]


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

amigos_info_dt = dt.fread('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-09-08/friends_info.csv')

amigos_info_dt

amigos_info_dt[:,count(),by(f.season)]

amigos_info_dt[:,count(),by(f.season,f.episode)
              ][:,{'unique_episodes':count()},by(f.season)
               ]

amigos_info_dt[:,dt.mean(f[-2:]),by(f.season)]

amigos_info_dt

amigos_info_dt[f.imdb_rating==dt.max(f.imdb_rating),:]

amigos_info_dt[f.imdb_rating==dt.min(f.imdb_rating),:]

amigos_info_dt[:2,:,by(f.season),sort(-f.imdb_rating)]

amigos_info_dt[f.title=="The Last One",:]

amigos_info_dt[[slice(None,235)],:]

amigos_info_dt[:4,:]

alt.Chart(amigos_info_dt[:,[f.season,f.episode,f.us_views_millions]].to_pandas()).mark_point().encode(
    alt.X('episode'),
    alt.Y('us_views_millions'))

directors_views_rating = amigos_info_dt[:,dt.mean(f[-2:]),by(f.directed_by)
              ][:,:,dt.sort(-f.imdb_rating)]

directors_dt = amigos_info_dt[:,count(),by(f.directed_by)][:10,:,dt.sort(-f.count)]

directors_dt.key='directed_by'

directors_views_rating

directors_views_rating[:,:,dt.join(directors_dt)][~dt.isna(f.count),:][:,:,dt.sort(-f.count)]

amigos_info_dt[f.directed_by=="Robby Benson",:]

amigos_info_dt[f.directed_by=="Michael Lembeck",:]

amigos_info_dt[:,dt.update(temp=f.directed_by==f.written_by)]

amigos_info_dt[f.temp==True,:]

todo_list = list()
for elemento in amigos_info_dt[:,f.written_by].to_list()[0]:
    todo_list.append(elemento.split('&'))

amigos_info_dt[f.title=="The One Where Estelle Dies",:]

num_or_writers = dt.Frame({'no_of_writers':[len(elem) for elem in todo_list]})

del amigos_info_dt["temp"]

amigos_info_dt_v1 = dt.cbind(amigos_info_dt,num_or_writers)

amigos_info_dt_v1[:,count(),by(f.no_of_writers)]


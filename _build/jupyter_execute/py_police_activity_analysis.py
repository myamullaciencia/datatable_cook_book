# Importing libraries
import datatable as dt
import pandas as pd
import altair as alt
from datatable import f,by,count,update,sort,join

dt.init_styles()
dt.options.display.head_nrows=4
dt.options.display.tail_nrows=4

policia_dt = dt.fread('https://assets.datacamp.com/production/repositories/1497/datasets/62bd9feef451860db02d26553613a299721882e8/police.csv',na_strings=[""])

weather_dt = dt.fread('https://assets.datacamp.com/production/repositories/1497/datasets/02f3fb2d4416d3f6626e1117688e0386784e8e55/weather.csv',na_strings=[""])

policia_dt

weather_dt

# count the number of missing values
policia_dt.countna()

del policia_dt[:,['county_name', 'state']]

policia_dt

policia_dt[:,count(),by(f.driver_gender)]

policia_tidy_dt = policia_dt[~dt.isna(f.driver_gender),:]

policia_tidy_df = policia_tidy_dt.to_pandas()

policia_tidy_df.info()

policia_tidy_df

policia_tidy_dt[:,count(),by(f.violation)
               ][:,f[:].extend({'grand_tot':dt.sum(f.count)})
                ][:,f[:].extend({'prop':f.count/f.grand_tot})
                 ][:,f[:].remove(f.grand_tot),sort(-f.prop)
                  ]

policia_tidy_dt[:,count(),by(f.driver_gender,f.violation)
               ][:,f[:].extend({'group_tot':dt.sum(f.count)}),by(f.driver_gender)
                ][:,f[:].extend({'prop':f.count/f.group_tot})
                 ][:,f[:].remove(f[1])]

policia_tidy_dt[f.violation=="Speeding",:
               ][:,count(),by(f.driver_gender,f.stop_outcome)
                ][:,f[:].extend({'group_total':dt.sum(f.count)}),by(f.driver_gender)
                 ][:,f[:].extend({'prop':f.count/f.group_total})
                  ][:,f[:].remove([f[1]])]

policia_tidy_dt[:,count(),by(f.search_conducted)
               ]

policia_tidy_dt[:,count(),by(f.driver_gender,f.search_conducted)
               ][:,f[:].extend({'group_total':dt.sum(f.count)}),by(f.driver_gender)
                ][:,f[:].extend({'prop':f.count/f.group_total})
                 ][:,f[:].remove(f[1])]

policia_tidy_dt[~dt.isna(f.search_type),:
               ][:,count(),by(f.search_type)
                ]

policia_tidy_dt[dt.f.search_type.re_match("[\w\s\W]+Frisk"),:
               ][:,count(),by(f.driver_gender)]

policia_tidy_dt[:,count(),by(f.stop_duration)]

policia_tidy_dt[:,count(),by(f.stop_duration,f.is_arrested)
               ][:,f[:].extend({'group_total':dt.sum(f.count)}),by(f.stop_duration)
                ][:,f[:].extend({'prop':f.count/f.group_total})
                 ][:,f[:].remove(f[1])]

policia_tidy_dt[:,count(),by(f.driver_race,f.is_arrested)]


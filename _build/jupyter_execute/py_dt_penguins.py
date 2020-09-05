# Data wrangling and modeling on Penguins dataset using pydatatable

# Loading libraries 
import datatable as dt
from datatable import f,by,count,update,sort
import altair as alt
import pandas as pd
import numpy as np

# Confifuring a set of DT options
dt.init_styles()
dt.options.display.head_nrows=4
dt.options.display.tail_nrows=4

# Importing data from a github source
penguins_dt = dt.fread('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-07-28/penguins.csv')

# Glance at data
penguins_dt

# Check datatypes of DT columns
penguins_dt.stypes

# Check any NA's acroos all columns
penguins_dt.countna()

# Look at the number of unique values per column
penguins_dt.nunique()

# Displaying DT  names and their types
for cname,ctype in zip(penguins_dt.names,penguins_dt.stypes):
    print(f'{cname}- is a type of: {ctype} ')

# First five observations from 2 to 5 columns in DT
penguins_dt[:5,2:6]

# Last five observations from DT
penguins_dt[-5:,:]

# All observations for last 3 columns
penguins_dt[:,-3:]

# Filter out NA's from sex and body mass g columns
penguins_dt[(dt.isna(f.sex) & ~dt.isna(f.body_mass_g)),:]

# mean of all numerics columns per different penguin sex categories
penguins_dt[~dt.isna(f.sex),:
           ][:,dt.mean((f[dt.int32].remove(f.year),f[dt.float64])),by(f.sex)]

# step - 1 : finding a max value of body_mass of penguins per sex
penguins_dt[:,update(temp=f.body_mass_g==dt.max(f.body_mass_g)),by(f.sex)]

# step - 2 : finding a max value of body_mass of penguins per sex
penguins_dt[f.temp==1,f[:].remove(f.temp)]

# step - 1 : finding a min value of body_mass of penguins per sex
penguins_dt[:,update(temp=f.body_mass_g==dt.min(f.body_mass_g)),by(f.sex)]


penguins_dt[f.temp==1,f[:].remove(f.temp)]

del penguins_dt["temp"]

penguins_tidy_dt = penguins_dt[~dt.isna(f.sex),:]

penguins_year_island = penguins_tidy_dt[:,{'total':count()},by(f.year,f.island)]

penguins_year = penguins_year_island[:,{'gr_total':dt.sum(f.total)},by(f.year)]

penguins_year

penguins_year.key="year"

penguins_year_island = penguins_year_island[:,:,dt.join(penguins_year)]

penguins_year_island[:,update(perc=f.total/f.gr_total)]

penguins_year_island

alt.Chart(penguins_year_island.to_pandas()).mark_bar(
).encode(
    alt.Y('year:O'),
    alt.X('total'),
    alt.Color('island')
).properties(title='Island existance over the years'
            )

penguins_island_spec_summary = penguins_tidy_dt[:,{'total':count()},by(f.year,f.island,f.species)]

alt.Chart(penguins_island_spec_summary.to_pandas()).mark_bar(
).encode(
    alt.Y('year:O'),
    alt.X('total'),
    alt.Color('island')
).facet('species',columns=2)

penguins_gender_species_summary = penguins_tidy_dt[:,{'total':count()},by(f.sex,f.island,f.species)]

alt.Chart(penguins_gender_species_summary.to_pandas()).mark_bar().encode(
    alt.X('species'),
    alt.Y('total'),
    alt.Color('sex')
).properties(
    height=300,width=350,title='Penguins over different Islands'
).facet('island',columns=3)

penguins_sel_dt_1 = penguins_tidy_dt[:,[f.flipper_length_mm,
                              f.bill_length_mm,
                              f.sex,
                              f.body_mass_g,
                              f.species]].to_pandas()

alt.Chart(penguins_sel_dt_1).mark_point(
).encode(
    alt.X('flipper_length_mm'),
    alt.Y('bill_length_mm'),
    alt.Color('sex')
).properties(
    height=200,
    width=250
).facet('species').configure_mark(opacity=0.6)

# select only numeric columns from DT
penguins_numericos_dt = penguins_tidy_dt[:,(f[dt.int32].remove(f.year),f[dt.float64])]

penguins_numericos_dt

alt.Chart(penguins_numericos_dt.to_pandas()).mark_point().encode(alt.X('bill_length_mm'),alt.Y('bill_depth_mm'))

peng_names = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm','body_mass_g']

alt.Chart(penguins_numericos_dt.to_pandas()).mark_circle().encode(
    alt.X(alt.repeat("column"), type='quantitative'),
    alt.Y(alt.repeat("row"),type="quantitative")
).properties(width=200,height=200).repeat(
    row=peng_names,
    column=peng_names[::-1]
).interactive()

penguins_tidy_dt

def py_tidy_descriptive_stats(DT):
    """Generate summary statistics of datatable"""
    datos_dict = DT.to_dict()
    summary_stats_of_dict = { k:[np.nanmean(v),
                                 np.nanmedian(v),
                                 np.nanmin(v),
                                 np.nanmax(v),
                                 np.nanstd(v),
                                 np.percentile(v,25,interpolation='midpoint'),
                                 np.percentile(v,75,interpolation='midpoint'),
                                 np.percentile(v,75,interpolation='midpoint')-np.percentile(v,25,interpolation='midpoint'),
                                 np.nanstd(v)/np.sqrt(np.shape(v)[0])] for k,v in datos_dict.items() }
    summary_dict_names = dt.Frame({'descriptive_stats':['Mean','Median','Min','Max','Std','Q1','Q3','IQR','SE']})
    summary_stats_of_dict_prep = {k:list(map(lambda x:np.round(x,3),v)) for k,v in summary_stats_of_dict.items()}
    summary_stat_dt = dt.Frame(summary_stats_of_dict_prep)
    return dt.cbind(summary_dict_names,summary_stat_dt)

py_tidy_descriptive_stats(penguins_numericos_dt)

penguins_sex_num = dt.cbind(penguins_numericos_dt,penguins_tidy_dt[:,f.sex])

alt.Chart(penguins_sex_num[:,(f.flipper_length_mm,f.sex)].to_pandas()).mark_bar().encode(alt.X('flipper_length_mm',bin=True),y='count()').facet('sex')

alt.Chart(penguins_sex_num[:,(f.bill_length_mm,f.sex)].to_pandas()).mark_bar().encode(alt.X('bill_length_mm',bin=True),y='count()').facet('sex')

alt.Chart(penguins_sex_num[:,(f.body_mass_g,f.sex)].to_pandas()).mark_bar().encode(alt.X('body_mass_g',bin=True),y='count()').facet('sex')


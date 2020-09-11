# Py : Tidy data analysis - Global Crop Yields

**Introduction** :

Our data on agricultural yields across crop types and by country are much more extensive from 1960 onwards. The UN Food and Agricultural Organization (FAO) publish yield estimates across a range of crop commodities by country over this period. The FAO report yield values as the national average for any given year; this is calculated by diving total crop output (in kilograms or tonnes) by the area of land used to grow a given crop (in hectares). There are likely to be certain regional and seasonal differences in yield within a given country, however, reported average yields still provide a useful indication of changes in productivity over time and geographical region.

# Importing libraries
import datatable as dt
import pandas as pd
import altair as alt
from datatable import f,by,count,update,sort,join
import re
from itertools import repeat
from itertools import chain

# Datatable options are set to display limit number of rows and datatable frame columns colors are maintained
dt.init_styles()
dt.options.display.head_nrows=4
dt.options.display.tail_nrows=4

crop_yields_global_dt = dt.fread('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-09-01/key_crop_yields.csv')

crop_fields = crop_yields_global_dt.names

crop_fields_clean = [re.sub('\s{1,}\([\w\s]+\)','',col).lower() for col in crop_fields ]

crop_fields_clean_1 = [ re.sub('\s','_',col) for col in crop_fields_clean ]

crop_yields_global_dt.names = crop_fields_clean_1

crop_yields_global_dt

crop_yields_global_dt_v1 = crop_yields_global_dt[:,dt.sum(f[3:]),by(f.entity)]

crop_yields_global_dt_v1

crop_fields_clean_1[3:]

def pydt_reshape_wide_to_long(DT,*measure_vars,var_name=None,val_name=None):
    """reshaping datatable from wide columns to long """
    dt_cols=[*measure_vars]
    measure_col_dict = DT[:,[*measure_vars]].to_dict()
    variables_dict={'variable':[],'value':[]}
    for k,v in measure_col_dict.items():
        variables_dict['variable'].extend(repeat(k,len(v)))
        variables_dict['value'].extend(v)
    wide_to_long_dt = dt.Frame(variables_dict)
    removed_cols_dt = DT[:,f[:].remove([ f[col] for col in dt_cols])].to_dict()
    non_measures_dt = dt.Frame({k:list(chain.from_iterable(list(repeat(v,len(dt_cols))))) for k,v in removed_cols_dt.items()})
    
    if var_name and val_name is not None:
        wide_to_long_dt.names={'variable':var_name,'value':val_name}
        
    wide_to_long_prep_dt=dt.cbind(non_measures_dt,wide_to_long_dt)
        
    return wide_to_long_prep_dt

crop_yields_tidy =pydt_reshape_wide_to_long(crop_yields_global_dt_v1,'wheat',
 'rice',
 'maize',
 'soybeans',
 'potatoes',
 'beans',
 'peas',
 'cassava',
 'barley',
 'cocoa_beans',
 'bananas',
var_name='crop',val_name='crop_yield')

crop_yields_tidy[:,dt.sum(f.crop_yield),by(f.crop)]


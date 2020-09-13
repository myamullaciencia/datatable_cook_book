# Regular expressions in python

import re
import datatable as dt
from datatable import f,by,count,update

### Section - 1: String Manipulations

#### 1.1 String operators

# example texts
text_1 = 'hola'
text_2 = 'como estas'
text_3 = 'hola cominante no hay camino se hace al andar'

# addition
text_1 + text_2

# multiplication
text_1*10

# multiplication negative
text_1 * -1

# in operator case - 1
'camino' in text_3

# in operator case - 2
'como' in text_3


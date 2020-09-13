# Python Regular expressions part - 1

### 1 . Introduction

import re

letra = 'espanolesun345'

'espanol' in letra

re.search(r'\s[\w]{2}\s','espanol es lenguage de 5 22 3 ')

text = 'La india esta en 209 posicion en covid 2019  covriance  violencia y hay poblacion de 5000 mil hoy' 

re.search(r'[0-9]{4}',text)

re.search(r'[0-9].\s',text)

### 2. Meta characters

###### 1. dot

**matches any single character except new line**

re.findall(r'h.y',text)

###### 2. Anchor(^)

**It matches at the start of string**

re.findall(r'^L[\w]+',text)

text[0:2]

###### 3. Anchor ($)

**It matches at the end of string**

re.findall(r'[a-z]{3}$',text)

###### 4. Repetitions(*)

**Matches zero or more repeats**

re.findall(r'\s[\d]*\s',text)

###### 5. Repititions(+)

**One or more repeats**

re.findall(r'cov+',text)

###### 6. Any(?)



1.   Matches zero or one repetition
2.   Specifies the non-greedy versions of *, +, and ?
3.   Introduces a lookahead or lookbehind assertion
4.   Creates a named group


re.findall(r'20[1]?9',text)

###### 7. Repeats ({})

**Matches an explicitly specified number of repetitions**

re.findall(r'[\d]{3,4}',text)

re.findall(r'[\w]{5}',text)



###### 8. Metacharacter(\\)

1. Escapes a metacharacter of its special meaning
2. Introduces a special character class
3. Introduces a grouping backreference

re.findall(r'\s[\d]{2}',text)

###### 9. Specifies a character class []


re.findall(r'[cov][\w]+',text)

###### 10. Creates a group

re.findall(r'(cov|ho)',text)

### 3. Examples

re.findall(r'cov[aeiou]','covariance')

re.findall(r'[0-9a-fA-F]','10 A B C X')

re.findall('[^0-9]','2020como')

re.findall(r'[\-123]','mall-123')

re.search(r'[\-c]','ma-c')

re.findall(r'123\]','mallesh 123]')

re.findall(r'h.y','hoy o hay')

re.findall(r'h.y','h\ny')

re.search(r'[\w]','$%@#a*&')

re.search(r'[\W]','$%@#a*&')

re.findall(r'[\W]','$%@#a*&')

re.findall(r'\d{3}',text)

re.search(r'\D{2}','20 viente')

re.findall(r'\s{2}','espanol como')

re.findall(r'h\.y','h.y')

re.search(r'word\b','do you have words to speak word')

re.findall(r'word\b','do you have word to speak words')

re.findall(r'\bword\b','do you have word to speak words')

re.search(r'\Bzip\B','EEzipRR')

re.search(r'(yup)*','yup yup hurr')

re.search(r'[0-9]-*[0-9]','2-3')

re.search('foo\.*bar', 'foo.bar')

re.search('foo\.?bar','foo.bar')

re.search('a{3,5}?', 'aaaaaaaa')

re.findall('a{3,5}?','aaaaaaaa')

re.findall(r'(covid)+','covid covid 2019 es una pandemica')

re.findall(r'covid','covid covid 2019 es una pandemica')

re.findall(r'cov+','covvvvvvvvriance')

re.findall(r'(cov)+','covcovcov')

re.search(r'foo(bar)?','foo')

re.search(r'(foo(bar)?)+','foofoobarbarfoobarfoobar')

re.findall(r'(\d\d\d)?','23')

regex = r'(\w+),(\d+),\2'

m = re.search(regex,'foo,1,1,foo')

### 5. Lookahead and Lookbehinds

# look aheads
rgx_positive_ahead = r'espanol(?=[\#]{2})'
rgx_negative_ahead = r'espanol(?![\#]{2})'

re.search(rgx_positive_ahead,'espanol##')

re.search(rgx_negative_ahead,'espanol')

# look behinds
rgx_positive_behind = r'(?<=[\#])[\w]+'
rgx_negative_behind = r'(?<![\#]{1})\d+'

re.search(rgx_positive_behind,'#myamulla')

re.findall(rgx_negative_behind,'####4#4#5#95')

# pos ahead
re.search(r'espanol(?=spanish)','espanolspanish')

# neg ahead
re.search(r'espanol(?!english)','espanolspanish')

# pos behind
re.search(r'(?<=Mr\.)[\w]+','Mr.Mallesham')

# neg behind
re.search('(?<!Sr\.)bar', 'Srta.bar')
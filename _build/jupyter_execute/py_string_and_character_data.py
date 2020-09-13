# Python String and Character data 

### 1.1 Basic string operations

text_1 = 'hola'
text_2 = 'como estas'
text_3 = 'no hay camino se hace al andar'

# adding two strings
text_1 + text_2

# repeat the string for a nu.of times
text_1 * 3

# is is OK to give negative number?
text_1 * -3

# How to check a word in a given text
'camino' in text_3

# how to check a word not in text
'caminar' not in text_3

# join two strings
','.join([text_1,text_2])

# Convert an integer to string
num_1 = 59
chr(num_1)

# convert a string to integer
ord(';')

# length of a text
len(text_3)

# returns a string representation of object
str(50)

### 1.2 String Indexing

# example string
text_4 = 'realpython'

# select letters from 3rd index onwards
text_4[3:]

# select first 3 letters
text_4[:3]

# select second letter in between of 2 and 7 letters
text_4[2:8:2]

### 1.3 Built-in String Methods

# define text
text_5 = 'cienciadedatos'
text_6 = 'Estadistica'

# Make first letter to capital
text_5.capitalize()

# Make first letter to small
text_6.lower()

# swap from capital to small, small to capital - 1
text_5.swapcase()

# swap from capital to small, small to capital - 2
text_6.swapcase()

# make a text as title text
text_5.title()

# convert small letters to upper letter
text_6.upper()

# Count how many of times a letter is appeared - 1
text_5.count('a')

# Count how many of times a letter is appeared in the specified index - 2
text_5.count('e',2,5)

# check a word starts with a specific letter
text_5.startswith('c')

# check a word ends with a specific letter
text_5.endswith('s')

# At which index a given letter is exist - 1
text_6.find('di')

# At which index a given letter is exist - 2
text_6.find('de')

# returns an index of specified letter
text_6.rindex('i')

text_6

### 1.4 Character Classification

# define a text
text_7 = 'Srciencia@2020'

# check if it is an alphanumeric
text_7.isalnum()

# check if it is an alphanumeric
text_7[:9].isalnum()

# check if it is a digit
text_7[10:].isdigit()


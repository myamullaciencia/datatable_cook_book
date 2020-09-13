# Python Regular expressions exercises

import re

### 1. Expressions

##### 1. Validation

bool(re.search(r'hola','holacomoestas'))

def has_vowel(text):
    pat = re.search('[aeiou]',text)
    return bool(pat)

has_vowel('ambrella')

has_vowel('nytms')

def is_integer(number):
    pattern = re.search('^\-?\d+$',number)
    return bool(pattern)

is_integer('4.4')

def is_fraction(number):
    pattern = re.search('^\-?\d+\/\d+$',number)
    return bool(pattern)

is_fraction('100')

is_fraction('345/2')

def get_extensions(text):
    pattern = re.findall(r'\.[\w]+$',text)
    return pattern

get_extensions('word.dox')

get_extensions('abcd.html')

get_extensions('red.zip')

def get_hexadecimal(word):
    pattern = re.findall(r'[ABCDEF]',word)
    return pattern

get_hexadecimal('ABE')

def get_tetravocalic(word):
    pattern = re.search(r'[aeiou]{4}',word)
    return bool(pattern)

get_tetravocalic('aaya')

def get_hexaconsonental(word):
    pattern = re.search(r'[^aeiouy]{6,}',word)
    return bool(pattern)

get_hexaconsonental('jkrtmnp')

def five_repeats(word):
    pattern = re.findall(r'(\w)\1*',word)
    return pattern

def is_number(num):
    pattern = re.search(r'')
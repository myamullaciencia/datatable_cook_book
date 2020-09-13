# Python Regular expressions exercises

import re

### 1. Validations and Search 

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
    return [ letter.group() for letter in re.finditer(r'(.)\1{4}',word)]

def is_number(num):
    pattern = re.search(r'\b[0-9]+\b',num)
    return bool(pattern)

five_repeats('MMMMMYAMULLAPPPPP')

def get_abbrevation(text):
    word_splits = re.split(r'\s',text)
    return ''.join([ w[0] for w in word_splits])

get_abbrevation('Hyper Text Markup Language')

get_abbrevation('Frequently Asked Questions')

def is_hex_color(color):
    busqueda =re.search(r'^[\#]([0-9a-f]{3}|[0-9a-f]{6})$',color)
    return bool(busqueda)

is_hex_color('#decafz')

is_hex_color('#9f2')

def is_valid_date(fecha):
    date_reg = re.compile(r'[0-9]{4}\-([0][0-9]|1[0-2])\-[0-3]{2}')
    return bool(date_reg.search(fecha))

is_valid_date("2016-01-02")

is_valid_date("1980-30-05")

is_valid_date("2016-02-99")

def repeaters(text):
    rep_rgx = re.compile(r'\b([A-Za-z]+)\1\b')
    return [ word.group() for word in rep_rgx.finditer(text)]

repeaters('cancan REXREX TOMTOM murmur TATA HAND CANCAN')

def normalize_jpeg(text):
    return re.sub(r'[E|e]','',text)

normalize_jpeg('Avatar.JPEG')

normalize_jpeg('AVATAR.Jpg')


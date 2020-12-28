# Py: Exercise - Count words

We want you to write a function that accepts a string and returns a mapping (a dictionary or dictionary-like structure) that has words as the keys and the number of times each word was seen as the values.

1. As a bonus, make sure the function works well with mixed case words

2. For even more of a bonus try to get the function to ignore punctuation outside of words.

# Import libraries
import re
from collections import Counter

# case 1
def count_words_case_1(text):
    text_split = re.split(r'\s',text)
    word_counts={}
    for w in text_split:
        if w in word_counts:
            word_counts[w]+=1
        else:
            word_counts[w]=1
    return word_counts

count_words_case_1('real python course is a real course')

# case 2
def count_words_case_2(text):
    text_split = re.split(r'\s',text)
    word_counts={}
    for w in text_split:
        word_counts.setdefault(w,0)
        word_counts[w] +=1
    return word_counts

count_words_case_2('pydatatable is a great data manipulation tool, pydatatable is built based on r datatable')

# case 3
def count_words_case_3(text):
    text_split = re.split(r'\s',text)
    return dict(Counter(text_split))

count_words_case_3('Python and R are great tools for data science, tools are always tools')

# case 4
def count_words_case_4(text):
    text_split = re.split(r'\s',text)
    text_small = [ word.lower() for word in text_split]
    return Counter(text_small)

count_words_case_4('Python R python r JAVA')

# case 5
def count_words_case_5(text):
    text_split = re.findall(r'\b[\w\-]+\b',text.lower())
    return Counter(text_split)

count_words_case_5('Dear Students,py-data US will be hosted on-line in 2020')
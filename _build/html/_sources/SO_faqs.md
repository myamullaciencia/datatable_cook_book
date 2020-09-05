Frequently Asked Questions
=======================

### 1. How to sort a datatable frame column in ascending/descending order

```
In [1]: import datatable as dt                                                                                                                   

In [2]: from datatable import f, sort                                                                                                            

In [3]: A = dt.Frame(product=["apples", "spam", "goo", "bobcat", "gold"],  
   ...:                  totals=[5.4, 2.777, 0.1, 2.9, 11.1])                                                                                    

In [4]: A[:, :, sort(-f.totals)]                                                                                                                 
Out[4]: 
   | product  totals
-- + -------  ------
 0 | gold     11.1  
 1 | apples    5.4  
 2 | bobcat    2.9  
 3 | spam      2.777
 4 | goo       0.1  

[5 rows x 2 columns]
```

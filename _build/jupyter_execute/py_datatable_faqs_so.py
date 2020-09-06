# py_datatable wiki 

import datatable as dt
from datatable import f,by,count,sum,update,sort
dt.init_styles()

## 1. Data Manipulations

### 1. 1 How to sort a datatable frame in descending order.?

We have created a sample dataframe with two columns such as product(character type) and totals(numeric type) using a frame object from dt and assigned it to a variable called X.

X = dt.Frame(product=["apples", "spam", "goo", "bobcat", "gold"], 
                 totals=[5.4, 2.777, 0.1, 2.9, 11.1])

X

As you might have already know about the datatable syntax as below 



                                        DT[I,J,BY|SORT|JOIN]
                                        
                                       
                                       
                                       
                                       
For now look at the sort function, it takes eigther a single column or multiple columns in, and it would be applicable for character and numeric type fields


1. In below code chunk case-1 we have passed a column totals in sort so that it arranges the data frame in ascending order considering the column(total).

2. In code chunk case-2 the same column is given with appending a symbol(-) so that it arranges the data frame in descending order considering the column(total).

3. In code chunk case - 3 we are trying to arrange the dataframe in ascending order of the products column

# case - 1
X[:,:,sort(f.totals)]

# case - 2 
X[:,:,sort(-f.totals)]

# case - 3
X[:,:,sort(f.product)]

Let us create a one more dataframe with repeated values of products as below

X = dt.Frame(products=['apples','spam','apples','gold','spam'],
             totals=[20,40,35,10,5])

We are now summing off the totals per each category of products and arrange it in descending order of newly created column tot_sum

X[:,{'tot_sum':sum(f.totals)},by(f.products)
 ][:,:,sort(-f.tot_sum)
  ]

### 1.2 How to count the number of instances for each category using group by in pydatadable?

Here is our basic syntax representation of datatable frame- 


                                        DT[I,J,BY|SORT|JOIN]

A sample dataframe created with the column name **languages** and would like to count how many of students are interested in learning each language category using aggregations such as by along with count,min,max,mean etc etc..

Yes, its correct we should use a function called **count** to caluclate the number of observations and let us see how it works below. 

prog_lang_dt = dt.Frame(languages= ['html', 'R', 'R', 'html', 'R', 'javascript',
                                    'R', 'javascript', 'html'])

prog_lang_dt

prog_lang_dt[:,count(),by(f.languages)]

If we would like like to rename a count column as total it can be done as follows,

prog_lang_dt[:,{'total':count()},by(f.languages)]

**count** can also take a column name as argument and report how many of non-missing entries in that specific column. for this example we will create a new dataframe as Y.

data = """
       id|charges|payment_method
       634-VHG|28|Cheque
       365-DQC|33.5|Credit card
       264-PPR|631|--
       845-AJO|42.3|
       789-KPO|56.9|Bank Transfer
       """

# read the data
Y = dt.fread(data, na_strings=['--', ''])

Y[:,count(f.payment_method)]

Here its simpy shows the count of payment methods are 3 and the remaining 2 observations are ignored


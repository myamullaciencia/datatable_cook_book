# py_datatable Q & A Notebook

# Importing the necessary libraries
import datatable as dt
from datatable import f,by,count,sum,update,sort
dt.init_styles()
dt.options.display.head_nrows=4
dt.options.display.tail_nrows=4

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

### 1.3 How to type cast a dataframe column in pydatatable?

We will create a dataframe with four columns such as cust_id,sales,profit_perc, and default

sales_DT = dt.Frame(

    {"cust_id":[893232.43],
     
     "sales":[1234532],
     
     "profit_perc":['10.43'],
     
     "default":[1]
    }
)

Check the each column datatype as below - 

sales_DT.stypes

Here are some key points:

-  cust_id is a type of float but in general customer id should be eigther integer or string type

-  sales is a type of int, it should not always be an integer and it may also be in float types

-  profict_perc is a type of string, here it should be a float type

-  default is a type of int and it should be a bool

**Note** : We have a syntax to be followed when we are to converting a column datatype from one to another as below

                           DT['Column_name']= new data type (int,floar,str,bool)

First, we will now try to apply the above formula on conveting a column type from float(**cust_id**) to integer 

sales_DT['cust_id'] = int

Here, let us verify the same whether it has become an integer type or not ?

sales_DT.stypes

Yes, it is converted. similarily we can convert a type from int(**sales**) to float and check.

sales_DT['sales'] = float

We have a column default with int type and we can have it as bool type.

sales_DT['default'] = bool

sales_DT.stypes

So far we have seen the convertions from 

- int to float
- float to int 
- int to str 
- float to string 
- int to bool
- etc etc 

sales_DT

That is OK, you have noticed or tried converting a column from string to any other types **(int,float,bool)**

sales_DT['profit_perc'] = float

**Note** : String to other type converions are not yet implemented in datatable versions till 0.10.1 and they would be surely implemented in the upcoming versions.

### 1.4 How to select columns based on their data types?

We will import a data from a specified URL source for this example as-

spotify_songs_dt = dt.fread('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv')

Datafram dimensions(rows,columns) can be checked as below

spotify_songs_dt.shape

Spotify dataframe has come with about 32K observations and 23 columns and the columns types can be viewed as

spotify_songs_dt.stypes

We would just like to take a look at the fields which are an any  type of ( int or string or bool or float ) etc etc. let us understand how it can be achived in py-datatable. we are already familiarized with datatable I,J sytax style as below. In J would always be made use to select the columns based  on given names or indices etc etc.. The required datatypes should be entered in the J expression so that it will display the respective observations.

                                DT[:,J]

Well, In a first attempt let us retrive the observations for all the interger columns as - 

spotify_songs_dt[:,dt.int32]

In a second attempt, we would like to see both float and bool type columns, and the below is the solution for it.

spotify_songs_dt[:,[dt.float64,dt.bool8]]

So here we have learnt that if more than one type of columns are required to be selected the types should be passed in J expression using a list i.e [dt.int32,dt.str32,dt.bool8] 

**Note** : In above two cases we have limited the output observations for 5 only. 

### 1.5 How do deselect columns from dataframe?

Deselecting the columns from dataframe is as important as selecting the columns. Deselection of columns can be done in J position itself specifying a function called **removed** along with the f expressions. let us look at the syntax first.

                DT[:,f[:].remove(cols to be kept a side)]

Here is our first example - deselect a column track_id from the spotify dataframe.

spotify_songs_dt[:,f[:].remove(f.track_id)]

In a second case - deselect these four columns(track_album_id,track_album_name,playlist_name,playlist_genre) from spotify dataframe - 

spotify_songs_dt[:,f[:].remove([f.track_album_id,f.track_album_name,f.playlist_name,f.playlist_genre])]

Here we have given a column names in a list and let us understand the anotomy of this syntax. 

- f[:]: it selects all the columns

- f[:].remove([f.x,f.y,f.z]) will deselect these three columns from others



What if our requirement is based on a type of column, of course it can also be achived with the same syntax as follows. and here we are deselecting all the string type columns from spotify dataframe.

spotify_songs_dt[:,f[:].remove(f[dt.str32])]

### 1.6 How to remove a list of columns from dataframe?

We already learnt how to deselect a list of columns, but here we are now going to see how to remove a list of columns from dataframe. and the below is the sytax for it.

            del DT[:,columns to be removed]

Let us create a sample dataframe as - 

comidas_gen_dt = dt.Frame({
    'country':list('ABCDE'),
    'id':[1,2,3,4,5],
    'egg':[10,20,30,5,40],
    'veg':[30,40,10,3,5],
    'fork':[5,10,2,1,9],
    'beef':[90,50,20,None,4]})

comidas_gen_dt

I would like to remove a column id from this dataframe following the above syntax - 

del comidas_gen_dt[:,"id"]

comidas_gen_dt

we noticed that the column id is no more existed in comidas dataframe, and if we want to remove more than one column their names should be passed in a list type as below-

del comidas_gen_dt[:,["veg","beef"]]

comidas_gen_dt

We are just left with 3 columns and i'm making a copy of this dataframe as - 

DT_comidas = comidas_gen_dt.copy()

DT_comidas is an independent from the comidas_gen_dt dataframe, means whatever the changes we make on comidas_get_dt those will not be replicated on DT_comidas and let us see how it is worked out.

From dataframe comidas_gen_gt we are going to remove a column fork as - 

del comidas_gen_dt[:,"fork"]

comidas_gen_dt

DT_comidas

Fork column is still available in DT_comidas and it is removed from comidas_gen_dt.

### 1.7 How to filter NA's from dataframe ?

datos = """
       id|charges|payment_method
       634-VHG|28|Cheque
       365-DQC|33.5|Credit card
       264-PPR|631|--
       845-AJO|42.3|--
       769-LPO|56.9|Gpay
       529-GPO|56.9|--
       903-QPO|--|--
       234-CPO|89.9|Bank Transfer
       102-PPO|26.9|Cash
       303-LPO|16.9|--
       692-CPO|--|PhonePay
       """

payments_dt = dt.fread(datos,na_strings=["--"])

We will have a sample dataframe for this case as below.

payments_dt

We have a function called **countna** from datatable, on applying it on dataframe it will count how many of NA's are in each column and returns a dataframe as below.

payments_dt.countna()

Here we have 2 NA's in charges column and 5 NA's in payment method.

As per the Datatable sytax we have a filter option I position as,

                           DT[I,:]

We can now call a function called **isna** from datatable, pass a column name whose NA's should be checked. For example we would like to filter NAs for a column charges as follows - 

payments_dt[dt.isna(f.charges),:]

What if we would like to not to include NA's observations per a column charges, and it can be done as follows- here we have just append that isna function with a symbol (~).

payments_dt[~dt.isna(f.charges),:]

We could also use the **isna** in by position to count how many of observations are having NA's per in specified column.

payments_dt[:,count(),by(dt.isna(f.payment_method))]

We have observed that there are 5 NA's and 6 observations are having the values.

There are some cases where we have to see two or more observations are together having the NA's. for example we can check for NA's across payment method and charges as below. we have made use of some logical operations and will be discussed when a case comes in. for now you can just remember this syntax.

payments_dt[:,count(),by((dt.isna(f.payment_method)) & (dt.isna(f.charges)))]

Here we can see that there is only one observation having NA's for both of these columns.

### 1.8 How to modify or update column values on a condition?

We are often required to modify the values of a column and it can be done following the below syntax -

        DT[I-specify filter condition, J-Specify column name] = New value

Assume we have a typo error in id columm for this observation **"102-PPO"**, and we want to change to to **103-PPO** - 

payments_dt[f.id=="102-PPO",f.id]="103-PPO"

and it can be viewed with a updated value.

payments_dt

We are now going to fill in NA's with a specific value in charges column as below. 

payments_dt[dt.isna(f.charges),f.charges]=20.45

payments_dt

### 1.9 How to add a new column to a dataframe ?

We add on some new columns to the dataframe as on when required, it can be achieved in two ways in py-datable.

1. a default value will be assigned to a newly created column

2. bindind a new dataframe columns to the existing dataframe.

Case 1: a new column **default** created with all True values

payments_dt['default'] = True

payments_dt

Case 2: we are going to bind the two dataframe columns as below

payment_default = dt.Frame(defalut_col=[True,False,True,False,True,False,False,True,False,False,True])

payments_new_dt = dt.cbind(payments_dt,payment_default)

payments_new_dt

Case 3: We are trying to bind two dataframes which are having unequal number of observations.

payment_default_1 = dt.Frame(defalut_col=[True,False,True,False,True,False,False,True,False,False])

payment_default_1.shape

dt.cbind(payments_dt,payment_default_1)

dt.cbind(payments_dt,payment_default_1,force=True)

**Note** : It is recommended that both dataframes should have the equal number of observations, however if they are not equally sized an extra option **force** should be passed in with an option **True**, so that the targeted observations are filled with NA's

### 1.10 How to add new observations to dataframe ?

# a dictionary with 5 key values
new_obs = {
    
    'id' : ['123-AMS','923-CIQ','100-ICIC'],
    'charges': [45.3,90.3,21.9],
    'payment_method': ['Gpay','Cheque','Ppay'],
    'default' : [False,False,False],
    'def_col':[False,True,False]
    
}

# new dataframe created
payment_extra_dt = dt.Frame(new_obs)

payment_extra_dt

We are now going to bind the rows of these two dataframes, here notice that the col **def_col** not existed in payments_new_dt, and let us see how this can be handled  below.

dt.rbind(payments_new_dt,payment_extra_dt)

dt.rbind(payments_new_dt,payment_extra_dt,force=True)

**Note** : It is recommended that both dataframes should have the same columns, however if they are not same an extra option **force** should be passed in with an option **True** so that the column values will be filled in with NA's.

### 1.11 How to rename column names of dataframe?

There are couple of typo errors in column names such as in the below dataframe we have a column **defalut_col** which have a spelling mistake and it should be renamed to **default_col**.

payments_new_dt

# list out the DT column names
payments_new_dt.names

# Change the column names using a dict {'old_col':'new_col'}
payments_new_dt.names = {'defalut_col':'default_col'}

payments_new_dt

### 1.12 How to find unique values by group in dataframe?

DT_ventas = dt.Frame({'c_id':[1,2,1,2,3,2,4,2,4,5],
                      'cust_life_cycle':['Lead','Active','Lead','Active','Inactive','Lead','Active','Lead','Inactive','Lead']
                     })

DT_ventas

DT_ventas[:,count(),by(f.cust_life_cycle,f.c_id)
         ][:,{'unique_cids':count()},by(f.cust_life_cycle)]

### 1.13 How to filter observations for the multiple values passed in the I expression of pydatatable frame?

DT_films = dt.Frame({'film':['Don','Warriors','Dragon','Chicago','Lion','Don','Chicago','Warriors'],
                     'gross':[400,500,600,100,200,300,900,1000]
                    })

DT_films

DT_films[((f.film=="Don") | (f.film=="Chicago")),:]

# Loading libraries
import functools
import operator

films = ['Lion', 'Chicago', 'Don']

filter_cond = functools.reduce(operator.or_, (f.film == item for item in films))

DT_films[filter_cond,:]


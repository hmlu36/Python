import pandas as pd
   
# Intitialise lists data.
data = [{'a': 1, 'b': 2},
        {'a': 5, 'b': 10, 'c': 20}]
   
# With two column indices, values same 
# as dictionary keys
df1 = pd.DataFrame(data, index =['first',
                                 'second'],
                   columns =['a', 'b'])
   
# With two column indices with 
# one index with other name
df2 = pd.DataFrame(data, index =['first',
                                 'second'],
                   columns =['a', 'b1'])
   
# print for first data frame
print (df1["a"], "\n")
   
# Print for second DataFrame.
print (df2)
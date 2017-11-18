## pandas

1. project_df.pivot(index=None, columns=None, values=None)

 > Docstring: Reshape data (produce a "pivot" table) based on column values. Uses unique values from index / columns to form axes of the resulting DataFrame.

2. pd.pivot_table(data, values=None, index=None, columns=None, aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All')

 > Docstring: Create a spreadsheet-style pivot table as a DataFrame. The levels in the pivot table will be stored in MultiIndex objects (hierarchical indexes) on the index and columns of the result DataFrame


2. df.replace(to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad', axis=None)

 > Docstring: Replace values given in 'to_replace' with 'value'.

3. pd.merge(left, right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False)

 > Docstring: Merge DataFrame objects by performing a database-style join operation by columns or indexes.
 If joining columns on columns, the DataFrame indexes *will be ignored*. Otherwise if joining indexes on indexes or indexes on a column or columns, the index will be passed on.
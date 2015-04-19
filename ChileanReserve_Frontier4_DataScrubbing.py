
# coding: utf-8

# # Restoration of Chilean eucalyptus plantation
# ## Data wrangling exercise using Python/pandas

# Goal is to take existing solution information and convert to Tableau-friendly format
# 
# Steps to get here:
# 
# 1. Model created by T. Walter, edits by N. Kullman
# 2. Frontier corner points (ideal solutions) solved individually using standalone CPLEX runs
# 3. Interior frontier pts found using Alpha Delta Program (calls CPLEX for optimization)
# 4. Dominated solutions removed
# 5. Solution files underwent one round of scrubbing through Java program built specifically for this task.
# 
# What's left (why we're here): Need all stands under a single column, rather than each having their own. And I want to learn data manipulation with Python/pandas.
# 
# Commence data manipulation...

# In[334]:

import pandas
import numpy
import pylab

from pandas import *
from pylab import *


# In[335]:

# read in and save solution data to dataframe
reserveSolns = read_csv('ADP_20150414_192212/FrontierSolutions_All_SolnYearID.csv')


# In[336]:

# Strip leading spaces from column names
reserveSolns = reserveSolns.rename(columns=lambda x: x.strip())


# In[337]:

# Stands are 'pivoted' across the table (col for each stand)
# Here we unpivot them, creating column for stand and prescription. This will require a merge.
# Merge's left is the original dataset, minus the stands columns
left = reserveSolns.ix[:,:"RI"]
# Merge's right is an unpivoted version of just the stands columns.
# Unpivoting done with the help of the melt function
right = pd.melt(reserveSolns,
                id_vars = ['Solution Index', 'Year'],
                # unpivot on the stands(first of which is XF502B)
                value_vars = reserveSolns.columns.tolist()[reserveSolns.columns.tolist().index("XF502B"):],
                var_name = 'Stand',
                value_name = 'Prescription')
# Merge to create our desired dataset
meltedReserveSolns = merge(left, right,
                           on = ["Solution Index", "Year"],
                           how = 'outer')


# In[338]:

# Convert prescription column vals to int
meltedReserveSolns["Prescription"] = meltedReserveSolns["Prescription"].apply(int)


# In[339]:

# Export to CSV for data viz with Tableau
meltedReserveSolns.to_csv('ReserveSolutions_Frontier4_AllPts.csv')


# We've finished what we set out to accomplish: learn some Python/pandas and clean a dataset for further analysis through visualization.

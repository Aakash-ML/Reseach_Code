import numpy as np
import pandas as pd
from pprint import pprint

# read data
df = pd.read_csv("GA_Data_with_TI.csv")
print("Data loaded !!")
pprint(df.head())
pprint(df.columns)
Today = 15
Shift_data_by = 5
#
indicators = [1,3,4,6,7]
def input_for_training(indicators):
    indicators = [i+Shift_data_by for i in indicators]
    sub_data = df.iloc[10:15,indicators]
    return list(sub_data.itertuples(index=False, name=None))

input_for_training(indicators)
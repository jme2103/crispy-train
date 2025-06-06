import pandas as pd
import numpy as np
import csv
import sys

pnd_file = sys.argv[1]
demo_file = sys.argv[2]
output_name = sys.argv[3]

# Load data
# _pnd file
npd = pd.read_csv(pnd_file)  # columns: partition, node, district
# _demomap.csv file
demo_data = pd.read_csv(demo_file)  # columns: ID, Red, Blue, Green, Population

# Rename 'ID' to 'node' for merging
if 'ID' in demo_data.columns:
    demo_data = demo_data.rename(columns={'ID': 'node'})

# List your demographic columns here, including the population column
demo_cols = ['Red', 'Blue', 'Green', 'Total']  

# Merge demographic data into npd for easy lookup
merged = npd.merge(demo_data, on="node")

# Group by partition and district, then sum demographic columns
grouped = merged.groupby(['partition', 'district'])[demo_cols].sum().reset_index()

grouped = pd.melt(grouped, id_vars=['partition', 'district'], var_name='color', value_name='population')

# Write to CSV
grouped.to_csv(output_name, index=False)
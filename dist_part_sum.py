import pandas as pd
import numpy as np
import csv

# Load data
npd = pd.read_csv("partitions.csv")  # columns: partition, node, district
demo_data = pd.read_csv("demo_data2.csv")  # columns: ID, Red, Blue, Green, Population

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
grouped.to_csv("partition_district_sums.csv", index=False)
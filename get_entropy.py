import pandas as pd
import numpy as np
import sys

target_file = sys.argv[1]

#add exception handling
def get_entropy(a, b):
    return (a / b) * np.log2(b / a) if a > 0 else 0

def get_proportional_entropy(population, total_population, entropy):
    return (population / total_population) * entropy if total_population > 0 else 0

#load data
information = pd.read_csv(target_file)#partitions, district, green, red, blue, total
#exclude total
info = information.drop(columns=['Total'])
#make it long 
info = pd.melt(info, id_vars=['partition', 'district'], var_name='color', value_name='population')


#append column which holds total population for each demographic group for the whole partition
total_pop = info.groupby(['partition', 'color'])['population'].sum().reset_index()




#we need an integer for the ratio of group to state population
partition_total_pop = total_pop['population'].head(3).sum()

info = info.merge(total_pop, on=['partition', 'color'], suffixes=('', '_total'))
print(info)
#calculate entropy for each group and district in the partition
info['entropy'] = info.apply(lambda row: get_entropy(row['population'], row['population_total']), axis=1)
print(info)


#sum and condense entropy for each partition and color
info = info.groupby(['partition', 'color'])['entropy'].sum().reset_index()
print(info)

info = info.merge(total_pop, on=['partition', 'color'], how='left')
print(info)

#info.join(total_pop.head(3), on=['color'], how='left')

info['proportional_entropy'] = info.apply(
    lambda row: get_proportional_entropy(row['population'], partition_total_pop, row['entropy']),
    axis=1
)
print(info)
#max value for n districts should be log2(3) = 1.585
#weve got values in excess of that here, what is going on?
final = info.groupby(['partition'])['proportional_entropy'].sum().reset_index()
final.to_csv('entropy.csv', index=False)
print("done")
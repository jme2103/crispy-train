import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

target_file = "partition_district_sums.csv"

#add exception handling
"""
def get_entropy(a, b):
    return (a / b) * np.log2(b / a) if a > 0 else 0

def get_proportional_entropy(population, total_population, entropy):
    return (population / total_population) * entropy if total_population > 0 else 0

#load data
information = pd.read_csv(target_file)#partitions, district, green, red, blue, total
#exclude total
info = information.drop(columns=['Total'])

print(info)

#make it long, changed previous code to do this, but will be nex=cessary for time being
#remove at a later date
info = pd.melt(info, id_vars=['partition', 'district'], var_name='color', value_name='population')

# print(info)

single_partition = info[info['partition'] == 0].copy()

# print(single_partition)

district_pop = single_partition.groupby(by=['partition', 'district'], sort=True, as_index=False)['population'].sum()
color_pop = single_partition.groupby(['partition', 'color'], sort=True, as_index=False)['population'].sum()
total_pop = single_partition['population'].sum()

# checks
# print(color_pop)
# print(district_pop)
# total_pop2 = color_pop['population'].sum()
# total_pop3 = district_pop['population'].sum()

print(info)
step0 = info[info['population'] > 0].copy()

step1 = step0.merge(district_pop, on=['district'], suffixes=('', '_district'))
# print(step1)
step1['proportion_of_district'] = step1['population'] / step1['population_district'] 
# print(step1)
step1['aux_step'] = step1['proportion_of_district'] * np.log2(1 / step1['proportion_of_district'])
# print(step1)

step2 = step1.groupby(['partition', 'color'], sort=True, as_index=False)['aux_step'].sum()
# print(step2)
step3 = step2.merge(color_pop, on=['color'], suffixes=('', '_color'))
print(step3)
step3['total_population'] = total_pop
print(step3)
step3['aux_step2'] = step3['aux_step'] * (step3['population'] / step3['total_population'])
print(step3)

step4 = step3.groupby(['partition'], sort=True, as_index=False)['aux_step2'].sum()
print(step4)

plt.hist(step4['aux_step2'], bins=10)
plt.show()

#############################

#append column which holds total population for each demographic group for the whole partition
total_pop = info.groupby(['partition', 'color'])['population'].sum().reset_index()




#we need an integer for the ratio of group to state population
partition_total_pop = total_pop['population'].head(3).sum()

info = info.merge(total_pop, on=['partition', 'color'], suffixes=('', '_total'))
# print(info)
#calculate entropy for each group and district in the partition
info['entropy'] = info.apply(lambda row: get_entropy(row['population'], row['population_total']), axis=1)
# print(info)


#sum and condense entropy for each partition and color
info = info.groupby(['partition', 'color'])['entropy'].sum().reset_index()
# print(info)

info = info.merge(total_pop, on=['partition', 'color'], how='left')
# print(info)

#info.join(total_pop.head(3), on=['color'], how='left')

info['proportional_entropy'] = info.apply(
    lambda row: get_proportional_entropy(row['population'], partition_total_pop, row['entropy']),
    axis=1
)
# print(info)
#max value for n districts should be log2(3) = 1.585
#weve got values in excess of that here, what is going on?
final = info.groupby(['partition'])['proportional_entropy'].sum().reset_index()
final.to_csv('entropy.csv', index=False)
print("done")

"""
import pandas as pd # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import sys
import time

target_file = sys.argv[1]
output_file = sys.argv[2]
cddc = int(sys.argv[3])
start_time = time.time()
#add exception handling

def entropy(dataframe, partition, x, y):
    print("something")
    single_partition = info[info['partition'] == 0].copy()
    x_pop = single_partition.groupby(by=['partition', x], sort=True, as_index=False)['population'].sum()
    y_pop = single_partition.groupby(['partition', y], sort=True, as_index=False)['population'].sum()
    total_pop = single_partition['population'].sum()

    #this is necessary to avoid division by zero
    step0 = info[info['population'] > 0].copy()
    
    #is it necessary to worry abou the x part of the equation at all?
    y_suffix = "_" + y
    step1 = step0.merge(y_pop, on=[y], suffixes=('', y_suffix))
    step1.drop(columns=[partition + "_" + y], inplace=True, errors='ignore')
    print("printing step1")
    print(step1)
    step1['proportion_of_y'] = step1['population'] / step1['population' + y_suffix]
    print(step1)
    step1['aux_step'] = step1['proportion_of_y'] * np.log2(1 / step1['proportion_of_y'])
    print(step1)
    step2 = step1.groupby([partition, y], sort=True, as_index=False)['aux_step'].sum()
    print(step2)
    step2 = step2.merge(y_pop, on=y, suffixes=('', '_' + y))
    step2.drop(columns=[partition + "_" + y], inplace=True, errors='ignore')
    print(step2)
    step2['proportional_entropy'] = step2['aux_step'] * (step2['population'] / total_pop)
    final = step2.groupby([partition], sort=True, as_index=False)['proportional_entropy'].sum()
    return final

#read into file
info = pd.read_csv(target_file)
#info.drop(columns=['Total'], inplace=True)
print(info)

#wide to long
#info = pd.melt(info, id_vars=['partition', 'district'], var_name='color', value_name='population')
print(info)

#feel  free to swap district and color or replace with any other value
#------------important stuff here----------------

if cddc == 1:
    info = entropy(info, 'partition', 'color', 'district')
if cddc == 0:
    info= entropy(info, 'partition', 'district', 'color')

print(info)

#export to csv
info.to_csv(output_file, index=False)

print("--- %s seconds ---" % (time.time() - start_time))

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
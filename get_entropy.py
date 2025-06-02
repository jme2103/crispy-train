import pandas as pd #type: ignore
import numpy as np #type: ignore
import sys

target_file = sys.argv[1]

x = sys.argv[2]
y = sys.argv[3]
#number of subsets of Y
size = int(sys.argv[4])

# Ent(X | Y)
#takes as arguments: the data frame with relevant data, name of partition column, almost always 'partition',
#names of X and Y columns, so like district or color, typically Y is color and x district
#output from previous functions should be like the following:
#partition, district, color, population
#population is the set (district U color), though we could use anything, not necessarily district or color
#when x is district and y is color, we get values for each intersection of district and color for each color first, then sum the values
#for each color proportionally to how much of the partiotion that group represents
#so what does it mean to do this categorically neutral?
def entropy(dataframe, partition, X, Y):
    #make list of total pop for each subset of Y
    # is the x even necessary?  no right?
    total_pops = dataframe.groupby([partition, Y])['population'].sum().reset_index()
    
    #integer, or at least a number?
    state_pop = total_pops[partition == 0]['population'].sum()

    dataframe = dataframe.merge((total_pops), on=[partition, Y] , suffixes=('', '_total'))

    #create new temp column for log function output
    dataframe["entropy"] = (dataframe['population'] / dataframe['population_total']) * np.log2(dataframe['population_total'] / dataframe['population'])
    #sum all the colors together for each partition
    dataframe = dataframe.groupby([partition, Y])['entropy'].sum().reset_index()

    info = info.merge(total_pops, on=[partition, Y], how='left')
    #calculate proportional entropy
    dataframe['proportional_entropy'] = (dataframe['population'] / state_pop) * dataframe['entropy']

    dataframe = dataframe.groupby([partition])['proportional_entropy'].sum().reset_index()
    return dataframe





#we can drop these
#add exception handling
"""
def get_entropy(a, b):
    return (a / b) * np.log2(b / a) if a > 0 else 0

def get_proportional_entropy(population, total_population, entropy):
    return (population / total_population) * entropy if total_population > 0 else 0

    
"""

#load data
information = pd.read_csv(target_file)#partitions, district, green, red, blue, total
#exclude total
info = information.drop(columns=['Total'])

print(info)

#make it long, changed previous code to do this, but will be nex=cessary for time being
#remove at a later date
info = pd.melt(info, id_vars=['partition', 'district'], var_name='color', value_name='population')

#run entropy funtion on the data
info = entropy(info, 'partition', x, y)
print(info)
info.to_csv('entropy_output.csv', index=False)
print("done")


"""
#append column which holds total population for each demographic group for the whole partition
total_pop = info.groupby(['partition', 'color'])['population'].sum().reset_index()




#we need an integer for the ratio of group to state population
partition_total_pop = total_pop['population'].head(3).sum()

info = info.merge(total_pop, on=['partition', 'color'], suffixes=('', '_total'))

#calculate entropy for each group and district in the partition
info['entropy'] = info.apply(lambda row: get_entropy(row['population'], row['population_total']), axis=1)



#sum and condense entropy for each partition and color
info = info.groupby(['partition', 'color'])['entropy'].sum().reset_index()
print(info)

info = info.merge(total_pop, on=['partition', 'color'], how='left')


#info.join(total_pop.head(3), on=['color'], how='left')

info['proportional_entropy'] = info.apply(
    lambda row: get_proportional_entropy(row['population'], partition_total_pop, row['entropy']),
    axis=1
)

#max value for n districts should be log2(3) = 1.585
#weve got values in excess of that here, what is going on?
final = info.groupby(['partition'])['proportional_entropy'].sum().reset_index()
final.to_csv('entropy.csv', index=False)
print("done")

"""
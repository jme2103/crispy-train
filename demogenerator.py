import numpy as np # type: ignore
from numpy import random # type: ignore
import pandas as pd # type: ignore
import sys

filename = sys.argv[1]
size = int(sys.argv[2])

demo_data = np.zeros((size * size, 5))

for i in range(len(demo_data)):
    demo_data[i, 0] = i
    
    #variance
    x_val = i % size 
    y_val = i / size
    variance = (1 / (size * size)) * (x_val * y_val)

    print(variance) 
    #red population
    mean = np.floor(1200 - 800 * variance)
    val = np.random.normal(mean, 200)
    demo_data[i, 1] = val
    demo_data[i, 1] = np.floor(demo_data[i, 1])
    #blue population
    mean = 1200 - 1000 * variance
    val = np.random.normal(mean, 200)
    demo_data[i, 2] = val
    demo_data[i, 2] = np.floor(demo_data[i, 2])
    #green population
    mean = 1200 - 1100 * variance
    val = np.random.normal(mean, 100)
    demo_data[i, 3] = val
    demo_data[i, 3] = np.floor(demo_data[i, 3])
    #total population
    demo_data[i, 4] = np.sum(demo_data[i, 1:4])

output = pd.DataFrame(demo_data, columns=["ID", "Red", "Blue", "Green", "Total"])
output.to_csv(filename + ".csv", index=False)

#np.savetxt("newcsv.csv", demo_data, delimiter=",", fmt="%d")

##
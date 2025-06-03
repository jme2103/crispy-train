import numpy as np # type: ignore
from numpy import random # type: ignore
import pandas as pd # type: ignore

demo_data = np.zeros((16, 5))

for i in range(len(demo_data)):
    demo_data[i, 0] = i

    #red population
    demo_data[i, 1] = np.floor(9 + random.rand() * 10)
    #blue population
    demo_data[i, 2] = np.floor(5 + random.rand() * 20)
    #green population
    demo_data[i, 3] = np.floor(8 + random.rand() * 15)
    #total population
    demo_data[i, 4] = np.sum(demo_data[i, 1:4])

output = pd.DataFrame(demo_data, columns=["ID", "Red", "Blue", "Green", "Total"])
output.to_csv("demo_data2.csv", index=False)

#np.savetxt("newcsv.csv", demo_data, delimiter=",", fmt="%d")

##
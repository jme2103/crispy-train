import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

target_file = sys.argv[1]


df = pd.read_csv(target_file)


df = df.drop(['partition'], axis=1)
print(df.head(20))
plt.hist(df)
plt.show()
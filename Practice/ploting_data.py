import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv('data/iris.csv')
data[4:].plot(kind='barh',rot=0)
plt.show()



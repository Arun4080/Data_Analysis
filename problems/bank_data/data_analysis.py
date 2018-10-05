import pandas as pd

a=pd.read_csv("a2p5z.csv",encoding="utf-8")
a.fillna(-99999,inplace=True)
print(a.head())

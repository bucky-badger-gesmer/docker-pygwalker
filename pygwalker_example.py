import pandas as pd
import pygwalker as pyg

df = pd.read_csv('./All-Star Selections.csv')
walker = pyg.walk(df)
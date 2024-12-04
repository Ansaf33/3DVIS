import pandas as pd   

def normalize(x,m,M):
  return 255*(x-m)/(M-m)


def add_popden_and_norm(df):
  df['POP_DENSITY'] = df['POPULATION'] / ( df['AREA'] * 3.861 * 1e-7 )
  m = df['POP_DENSITY'].min()
  M = df['POP_DENSITY'].max()
  df['NORM'] = df['POP_DENSITY'].apply(lambda x : normalize(x,m,M))
  
  return df
  
import pandas as pd  

def getlatlon(df,latcol,longcol):
  maxpopidx = df['NORM'].idxmax()
  lat = float(df.loc[maxpopidx,latcol])
  lon = float(df.loc[maxpopidx,longcol])
  return lat,lon 

  
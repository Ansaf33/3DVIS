import pandas as pd 
import geopandas as gpd 


# ----- GET THE STATE NAME 
def get_state_name(df):
  m = int(len(df)/2)
  separator = ',' if ',' in df.loc[m,'NAME'] else ';'
  state = df.loc[m,'NAME'].split(separator)[2]
  return state,separator
  

# ----- REMOVE UNNECCESSARY COLUMNS IN THE DATAFRAME 
def remove_unneccessary_columns(df):
  # REMOVE THE FINAL COLUMN
  df.drop(columns=['Unnamed: 3'],inplace=True)
  # REMOVE THE NAME COLUMN
  df.drop(columns=['NAME'],inplace=True)
  # AFTER REMOVING THE NAME COLUMN, REPLACE THE NUMBER COLUMN WITH THE NAME COLUMN
  df.rename(columns={'NUMBER':'NAME'},inplace=True)
   
  return df 

# ------- REMOVE USELESS INDICES IN THE DATAFRAME 
def remove_unnecessary_index(df,separator):
  # REMOVE THE INDEX THAT SAYS GEOGRAPHY
  df.drop(index = df[df['GEO_ID']=="Geography"].index,inplace=True)
  # REMOVE THE INDEX OF USA's POPULATION
  df.drop(index = df[df['NAME'] == "United States"].index,inplace = True)
  # REMOVE THE INDICES WHERE CENSUS TRACT IS NOT PRESENT ie NOT VALID 
  df.drop(index = df[ ~df['NAME'].str.contains("Census Tract") ].index,inplace=True)
  
  df.reset_index(inplace=True)
  
  return df 


# ------ RENAME COLUMNS 
def rename_columns(df,og,n):
  df.rename(columns={og:n},inplace=True)
  
  return df 

# ----- MODIFY POPULATION FROM TYPE TO STR
def modify_column(df,col,type):
  df[col] = df[col].astype(type)
  
  return df


# ------ ADD NUMBER AND COUNTY COLUMNS 


def add_name_and_county(df,separator):
  df['NUMBER'] = df['NAME'].apply(lambda x : x.split(' ')[2][:-1] )
  df['COUNTY'] = df['NAME'].apply(lambda x : x.split(separator)[1] )
  
  return df 


# ------ REMOVE INDICES WITH STATES OTHER THAN 'state'

def remove_other_states(df,state):
  df.drop(index=df[~df['NAME'].str.contains(state)].index,inplace=True)
  
  return df 
  
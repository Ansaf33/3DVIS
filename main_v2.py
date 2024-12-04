import pandas as pd
import geopandas as gpd 
import pydeck as pdk
import cleaner as cl 
import addinfo
import getinfo 

def generate_map(p,a,lat,lon,cp,shp):
  
# USER NEEDS TO ENTER THIS 
  og_popcol = p
  og_areacol = a
  og_latcol = lat
  og_longcol = lon

  census_path = cp
  shapefile_path = shp

  # ---------------------------------- CENSUS FILE 

  census = pd.read_csv(census_path)

  # GET THE STATE NAME 
  state,separator = cl.get_state_name(census)

  # REMOVE OTHER STATES
  census = cl.remove_other_states(census,state)

  # ADD NEW COLUMNS
  census = cl.add_name_and_county(census,separator)

  # REMOVE UNNECESSARY INDICES
  census = cl.remove_unnecessary_index(census,separator)

  # REMOVE UNNECESSARY COLUMNS
  census = cl.remove_unneccessary_columns(census)

  # RENAME COLUMNS
  census = cl.rename_columns(census,og_popcol,'POPULATION')

  # MAKE POPULATION INTEGERS
  census = cl.modify_column(census,'POPULATION',int)


  # ---------------------------------- SHAPE FILE 

  shape = gpd.read_file(shapefile_path)
  shape = cl.rename_columns(shape,og_areacol,'AREA')

  combined = shape.merge(census,how='left')

  json_path = 'data/'+state+'.json'
  combined.to_file(json_path,'GeoJSON')

  # ----------------------------------- JSON FILE ( CREATE NEW COLUMNS )

  ct_tracts = gpd.read_file(json_path)

  ct_tracts = addinfo.add_popden_and_norm(ct_tracts)


  # ---------------------------------- MAP CREATOR

  lat,lon = getinfo.getlatlon(ct_tracts,og_latcol,og_longcol)

  IVS = pdk.ViewState(latitude=lat, 
                      longitude=lon, 
                      zoom=9, 
                      max_zoom=16, 
                      pitch=60, 
                      bearing=0)

  fill_color = "POPULATION==0?[0,0,0,0]:[4*NORM+70,2*NORM+10,NORM+5]"
  line_color = fill_color

  layers = pdk.Layer(
      "GeoJsonLayer",
      ct_tracts,
      opacity=1,
      stroked=True,
      filled=True,
      extruded=True,
      wireframe=True,
      pickable=True,
      get_elevation="POP_DENSITY", 
      get_fill_color=fill_color,
      get_line_color=line_color,
  )

  map_3D = pdk.Deck(layers=[layers],initial_view_state=IVS)
  
  return map_3D

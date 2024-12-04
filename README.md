# 3D Map Visualizer

Created using PyDeck, GeoPandas with Streamlit working at the front.

Prerequisites:

## Census Tract CSV Files 

Some of these can be found at https://data.census.gov/table/DECENNIALDHC2020.P1?t=Population+Total%3AResident+Population&g=040XX00US09%241400000&tp=false.

- Any other legible CSV format is also applicable, however must contain the data similar to the following example : "Census Tract 101, County, State", The 101 being the primary key of the table.


## Shapefile in ZIP Format

These can primarily be found at https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2020&layergroup=Census+Tracts.

- Proper column names must be ensured. For instance, the NAME attribute used as foreign key for merging both the .shp and .csv files. 

- The relation must also have the following attributes for : **Latitude, Longitude, Land Area (in m^2), Geometry**
 
- Land area must be in m^2 *(Can change by adjusting the formula in the add_info.py file, line 8)*

- Algorithm is designed to use only the *'.shp'* file, so ensure that any other file with an extension named *'.shp'* has more extensions. *'.shp.'* is preferable for those.

## User Entry

- Users need to enter their column names for the attributes mentioned : **Latitude, Longitude, Land Area, Population**

## GET THE MAP 

run `streamlit run homepage.py`, which will direct you to a browser.

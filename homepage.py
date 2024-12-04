import streamlit as st 
import os 
import zipfile
import main_v2 as mapGenerator
from glob import glob
import shutil


  
def get_path_of_shp(folname):
  files = os.listdir('data/'+folname)
  for file in files:
    if '.shp' in file and '.shp.' not in file:
      return 'data/'+folname+file
  return None


def save_file(file,path):
  with open(path,"wb") as f:
    f.write(file.getbuffer())
    
def extract_file(zip_path,extract_path):
  zip_ref = zipfile.ZipFile(zip_path,'r')
  zip_ref.extractall(extract_path)
  all_files = zip_ref.namelist()
  return all_files[0]

def clear_files(path):
  for file in glob(path+'/*'):
    if os.path.isdir(file):
      shutil.rmtree(file)
    else:
      os.remove(file)
  return 1

st.title("3D GeoMap Visualization using PyDeck")

st.write("You only need 2 files to view your map. Let's proceed.")

st.write("Census Tract : Must contain a POPULATION field along with a NAME field titled <Census Tract Number> <separator> <County> <separator> <State>")

census_file = st.file_uploader("CSV File of the Census Tract",type="csv")


st.divider()

st.write("Shapefile for the state : Must contain the ID field, geometry field and a field that provides area in m^2")

shape_file = st.file_uploader("Zip File of the Shapefile",type="zip")

if census_file and shape_file:
  st.write("Uploaded both files.")
  
st.divider()
  
st.subheader("Kindly provide some details regarding the files you uploaded.")

st.write("Attribute name for Population (in the Census Tract File ) ")
og_popname = st.text_input("Enter Population Attribute Name")

st.write("Attribute name for Area (in the Shape File ) ")
og_areaname = st.text_input("Enter Area Attribute Name")

st.write("Attribute name for Latitude (in the Shape File ) ")
og_latname = st.text_input("Enter Latitude Attribute Name")

st.write("Attribute name for Longitude (in the Shape File) ")
og_lonname = st.text_input("Enter Longitude Attribute Name")

inputs = [census_file,shape_file,og_popname,og_areaname,og_latname,og_lonname]

generator = st.button("Generate Map")

if generator:
  # check if all files are uploaded
  for item in inputs:
    if not item:
      st.write("You haven't uploaded / provided all documents / fields. Kindly do so before proceeding.")
      break
    
  # all files are uploaded, proceed
  census_path = 'data/uploaded_census.csv'
  zip_path = 'data/shapefile.zip'
  
  # save the files, and extract them
  save_file(census_file,census_path)
  save_file(shape_file,zip_path)
  folder = extract_file('data/shapefile.zip','data')
  
  # identify the shapefile
  shapefile_path = get_path_of_shp(folder)
  
  map_3D = mapGenerator.generate_map(og_popname,og_areaname,og_latname,og_lonname,census_path,shapefile_path)
  
  
  output_path = 'data/3DMap.html'

  
  map_3D.to_html(output_path)
  
  # downloading the map
  
  with open(output_path, 'rb') as file:
    st.download_button(
        label="Download 3D Map",
        data=file,
        file_name="3DMap.html",
        mime="application/html"
    )
  
  # CLEAR ALL THE FILES INSIDE DATA 
  clear_files('data')
  
  
  
  
  
  
  


  

  
    

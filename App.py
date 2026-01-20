import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

st.set_page_config(page_title="Coordinate Converter", page_icon="🗺️")
st.title("Coordinate Converter")

COORDINATE_SYSTEMS = {
    "Lat/Lon (WGS84)": "EPSG:4326",
    "NZTM (EPSG:2193)": "EPSG:2193",
    "NZGD2000": "EPSG:4167",
    "NZGD1949": "EPSG:4272"
}

uploaded_file = st.file_uploader("Upload file", type=['csv', 'xlsx', 'xls'])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        st.dataframe(df.head())
        
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X / Longitude / Easting", options=df.columns)
        with col2:
            y_col = st.selectbox("Y / Latitude / Northing", options=df.columns)
        
        col3, col4 = st.columns(2)
        with col3:
            input_crs = st.selectbox("From", options=list(COORDINATE_SYSTEMS.keys()))
        with col4:
            output_crs = st.selectbox("To", options=list(COORDINATE_SYSTEMS.keys()))
        
        if st.button("Convert", type="primary"):
            df_clean = df.dropna(subset=[x_col, y_col])
            
            geometry = [Point(xy) for xy in zip(df_clean[x_col], df_clean[y_col])]
            gdf = gpd.GeoDataFrame(df_clean, geometry=geometry, crs=COORDINATE_SYSTEMS[input_crs])
            gdf_transformed = gdf.to_crs(COORDINATE_SYSTEMS[output_crs])
            
            df_clean['Converted_X'] = gdf_transformed.geometry.x
            df_clean['Converted_Y'] = gdf_transformed.geometry.y
            
            st.dataframe(df_clean.head())
            
            csv = df_clean.to_csv(index=False)
            st.download_button(
                "Download",
                data=csv,
                file_name="converted.csv",
                mime="text/csv",
                type="primary"
            )
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
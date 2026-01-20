import streamlit as st
import pandas as pd
from pyproj import Transformer

st.set_page_config(page_title="Lat/Lon to NZTM Converter", page_icon="🗺️")

st.title("Lat/Lon to NZTM Converter")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xlsx', 'xls'])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.dataframe(df.head())
        
        lat_col = None
        lon_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if col_lower in ['lat', 'latitude']:
                lat_col = col
            elif col_lower in ['lon', 'longitude', 'long']:
                lon_col = col
        
        if lat_col and lon_col:
            if st.button("Convert", type="primary"):
                transformer = Transformer.from_crs("EPSG:4326", "EPSG:2193", always_xy=True)
                
                nztm_coords = []
                for idx, row in df.iterrows():
                    try:
                        lat = row[lat_col]
                        lon = row[lon_col]
                        x, y = transformer.transform(lon, lat)
                        nztm_coords.append({'NZTM_X': x, 'NZTM_Y': y})
                    except:
                        nztm_coords.append({'NZTM_X': None, 'NZTM_Y': None})
                
                result_df = pd.concat([df, pd.DataFrame(nztm_coords)], axis=1)
                
                st.dataframe(result_df.head())
                
                csv = result_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="nztm_converted.csv",
                    mime="text/csv",
                    type="primary"
                )
        else:
            st.error("Could not find latitude and longitude columns")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
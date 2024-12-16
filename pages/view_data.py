import streamlit as st
import pandas as pd
from service.species_service import get_species_data
from service.tracking_record_service import get_tracking_data


st.header("View Data")
    
species_data = get_species_data()
if species_data:
    # Display species data (common_name, scientific_name)
    st.subheader("Species Data")
    species_df = pd.DataFrame(species_data)
    species_df = species_df[['species_id', 'species_name', 'scientific_name', 'conservation_status','category', 'image_url']]
    species_df['image_preview'] = species_df['image_url'].apply(
    lambda x: f'<img src="{x}" width="100" style="border-radius: 5px;"/>')
    html_table = species_df.to_html(escape=False, render_links=True)
    st.markdown(html_table, unsafe_allow_html=True)

tracking_data = get_tracking_data()
if tracking_data:
    # Display tracking data, ensuring we have species_id and related species information
    tracking_df = pd.DataFrame(tracking_data)
    tracking_df = tracking_df[['timestamp', 'species_id', 'location_id', 'count']]
    
    # Join with species data to display common_name and scientific_name alongside tracking data
    tracking_df = tracking_df.merge(species_df, how='left', left_on='species_id', right_on='species_id')
    tracking_df = tracking_df[['timestamp', 'species_id', 'species_name', 'scientific_name', 'location_id', 'count']]
    
    st.subheader("Tracking Data")
    st.dataframe(tracking_df)

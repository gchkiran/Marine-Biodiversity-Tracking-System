import streamlit as st
import pandas as pd
import plotly.express as px
from service.tracking_record_service import get_tracking_data

st.header("Data Visualization")

tracking_data = get_tracking_data()

if tracking_data:
    df = pd.DataFrame(tracking_data)

    # Plot the line chart
    fig = px.line(df, x='timestamp', y='species_name', title="Species Sightings Over Time", 
                    labels={'timestamp': 'Date', 'species_name': 'Species Name'})

    # Show the chart
    st.plotly_chart(fig)
    
    if 'latitude' in df.columns and 'longitude' in df.columns:
        # Plot locations on a map
        fig_map = px.scatter_mapbox(df, lat='latitude', lon='longitude', color='species_name', 
                                    hover_name='species_name', hover_data=['timestamp', 'count'],
                                    title="Species Locations", 
                                    color_continuous_scale=px.colors.cyclical.IceFire)

        # Set the mapbox style and center the map
        fig_map.update_layout(mapbox_style="carto-positron",
                              mapbox_zoom=5,  # Adjust the zoom level as needed
                              mapbox_center={"lat": df['latitude'].mean(), "lon": df['longitude'].mean()})

        # Show the map chart
        st.plotly_chart(fig_map)

    else:
        st.warning("No location data (latitude/longitude) found.")


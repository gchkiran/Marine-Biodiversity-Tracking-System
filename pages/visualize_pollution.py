import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit.components.v1 import html
from service.pollution_source_service import get_pollution_sources

st.header("Visualize Pollution Sources")
st.subheader("Pollution Sources Heatmap")

# Fetch pollution sources data from the service layer
pollution_sources = get_pollution_sources()

# Create a Folium map centered at latitude 0 and longitude 0 with an initial zoom level
m = folium.Map(location=[0, 0], zoom_start=2)

# Prepare heatmap data (latitude, longitude, pollutant level)
heatmap_data = [
    [source['latitude'], source['longitude'], source['pollutant_level']]
    for source in pollution_sources if source['latitude'] and source['longitude']
]

# Add HeatMap layer to the Folium map
if heatmap_data:
    HeatMap(heatmap_data, max_zoom=2).add_to(m)

# Save the Folium map to an HTML file
map_html_path = 'pollution_sources_map.html'
m.save(map_html_path)

# Embed the map HTML file into Streamlit
with open(map_html_path, 'r') as map_file:
    map_html = map_file.read()

# Display the map within Streamlit
html(map_html, height=600)

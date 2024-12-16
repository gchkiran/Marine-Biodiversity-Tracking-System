import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.express as px
import pydeck as pdk
from service.location_service import add_location, get_location_data

# Streamlit header
st.header("Manage Locations")
if 'locations' not in st.session_state:
    st.session_state.locations = []

if 'coordinates' not in st.session_state:
    st.session_state.coordinates = [15.0, 20.0]  # Default coordinates

# Inputs for the location name, latitude, longitude, and ecosystem type
location_name = st.text_input("Location Name")
latitude = st.number_input("Latitude", format="%.6f", value=st.session_state.coordinates[0], min_value=-90.0, max_value=90.0)
longitude = st.number_input("Longitude", format="%.6f", value=st.session_state.coordinates[1], min_value=-180.0, max_value=180.0)
ecosystem_type = st.selectbox("Ecosystem Type", ["Coral Reef", "Open Ocean", "Mangrove", "Estuary"])

# Define the map's view state with customized zoom level
view_state = pdk.ViewState(
    latitude=latitude,
    longitude=longitude,
    zoom=2,  # Lower zoom level for zooming out
    pitch=0,
)

# Create the map using pydeck with a scatterplot layer
deck = pdk.Deck(
    initial_view_state=view_state,
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame([{
                'lat': latitude,
                'lon': longitude
            }]),
            get_position=["lon", "lat"],
            get_color=[255, 0, 0],
            get_radius=100000,
            pickable=True,
        ),
    ],
    tooltip={"text": "{lat}, {lon}"},
)

# Display the map
st.pydeck_chart(deck)

# Instructions for selecting the location
st.write("Adjust the Latitude and Longitude to select a location.")

# Add a submit button to save the location
if st.button("Add Location"):
    if location_name:
        add_location(location_name, latitude, longitude, ecosystem_type)
        st.session_state.locations.append({
            'name': location_name,
            'ecosystem_type': ecosystem_type,
            'latitude': latitude,
            'longitude': longitude
        })
        st.success(f"Location '{location_name}' added successfully!")
    else:
        st.error("Please fill in the location name.")

# Display list of added locations
st.subheader("Added Locations:")
if len(st.session_state.locations) > 0:
    for idx, loc in enumerate(st.session_state.locations, start=1):
        st.write(f"{idx}. **{loc['name']}** - {loc['ecosystem_type']} - "
                f"Latitude: {loc['latitude']}, Longitude: {loc['longitude']}")
else:
    st.write("No locations added yet.")


location_data = get_location_data()
if location_data:
    st.subheader("Location Map")
    df = pd.DataFrame(location_data)
    
    view_state = pdk.ViewState(latitude=df['latitude'].mean(), longitude=df['longitude'].mean(), zoom=2)
    layer = pdk.Layer("ScatterplotLayer", data=df, get_position=["longitude", "latitude"], get_color=[0, 0, 255], get_radius=100000)
    
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
    st.pydeck_chart(deck)

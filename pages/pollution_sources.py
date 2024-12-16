import streamlit as st
from service.pollution_source_service import add_pollution_source
from service.location_service import get_location_data

st.header("Manage Pollution Sources")

pollution_source_name = st.text_input("Pollution Source Name")
pollution_type = st.selectbox("Pollution Type", ["Industrial Waste", "Agricultural Runoff", "Plastic Debris", "Chemical Spill", "Other"])
if pollution_type == "Other":
    pollution_type = st.text_input("Specify Pollution Type")

pollutant_level = st.number_input("Pollutant Level", min_value=0.0, max_value=10.0)
location_data = get_location_data()

if location_data:
    location_options = {l['location_name']: l['location_id'] for l in location_data}
    location_name = st.selectbox("Location Affected", list(location_options.keys()))
    location_id = location_options[location_name]
else:
    location_name = st.text_input("Location Name")
    location_id = None

if st.button("Add Pollution Source"):
    if pollution_source_name and location_name:
        add_pollution_source(pollution_source_name, pollution_type, location_id, pollutant_level)
        st.success(f"Pollution Source '{pollution_source_name}' added successfully!")

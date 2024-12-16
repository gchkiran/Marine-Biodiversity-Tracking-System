import streamlit as st
from service.tracking_record_service import add_tracking_record
from service.species_service import get_species_data
from datetime import datetime, timedelta
from service.location_service import get_location_data

today = datetime.today()
min_date = today - timedelta(days=365 * 100)


st.header("Add Tracking Record")

species_data = get_species_data()
if not species_data:
    st.error("No species data available!")
else:
    species_options = [f"{s['species_name']} ({s['scientific_name']})" for s in species_data]
    selected_species = st.selectbox("Species", species_options)

    if selected_species:
        species_id = next((s['species_id'] for s in species_data if s['species_name'] in selected_species), None)

        location_data = get_location_data()
        if location_data:
            location_options = {l['location_name']: l['location_id'] for l in location_data}
            location_name = st.selectbox("Location", list(location_options.keys()))
            location_id = location_options[location_name]
        else:
            location_name = st.text_input("Location Name")
            location_id = None

        timestamp = st.date_input("Date of Observation", value=today, min_value=min_date, max_value=today)        
        count = st.number_input("Count of Species", min_value=50)


        if st.button("Submit Record"):
            add_tracking_record(species_id, location_id, timestamp, count)
            st.success(f"Tracking record for species '{selected_species}' added successfully!")

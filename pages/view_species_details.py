import streamlit as st
import pandas as pd
import pydeck as pdk
from service.species_service import get_species_data, get_species_habitat_and_threat
from service.tracking_record_service import get_tracking_data
from service.pollution_source_service import get_pollution_sources
from service.environmental_factors_service import get_environmental_factors

# Function to get pollution data for a given location ID
def get_pollution_data(location_id):
    pollution_sources = get_pollution_sources()
    return [ps for ps in pollution_sources if ps['location_id'] == location_id]

# Streamlit page header
st.title("Species Details")

# Input for species name
species_query = st.text_input("Enter a species name or part of it:")

if species_query:
    # Fetch species data with the query
    species_data = get_species_data(species_query)

    if species_data:
        # Display species options
        species_options = [f"{s['species_name']} ({s['scientific_name']})" for s in species_data]
        selected_species = st.selectbox("Select a Species", species_options)

        # Extract the common name and scientific name from the selection
        common_name = selected_species.split(' (')[0]
        scientific_name = selected_species.split('(')[1][:-1]

        # Get species details
        species_data = next((s for s in species_data if s['species_name'] == common_name), None)
        
        if species_data:
            # Display species information
            st.subheader("Species Information")
            st.write(f"**Common Name:** {species_data['species_name']}")
            st.write(f"**Scientific Name:** {species_data['scientific_name']}")
            st.write(f"**Conservation Status:** {species_data['conservation_status']}")
            st.write(f"**Category:** {species_data['category']}")
            st.image(species_data['image_url'], caption="Species Image", use_column_width=False)

            # Fetch habitat and threat information
            habitat_threat_info = get_species_habitat_and_threat(species_data['species_id'])
            st.subheader("Habitat and Threat Information")
            st.write(f"**Habitat Type:** {habitat_threat_info['habitat_type'] if habitat_threat_info['habitat_type'] else 'N/A'}")
            st.write(f"**Habitat Description:** {habitat_threat_info['habitat_description'] if habitat_threat_info['habitat_description'] else 'N/A'}")
            st.write(f"**Threat Description:** {habitat_threat_info['threat_description'] if habitat_threat_info['threat_description'] else 'N/A'}")
            st.write(f"**Threat Severity:** {habitat_threat_info['threat_severity'] if habitat_threat_info['threat_severity'] else 'N/A'}")

            st.subheader("Migration Pattern")
            st.write(f"**Migration Pattern Description:** {habitat_threat_info['migration_pattern_description'] if habitat_threat_info['migration_pattern_description'] else  'N/A'}")


            # Fetch tracking records
            tracking_records = get_tracking_data()
            relevant_tracking_records = [record for record in tracking_records if record['species_name'] == common_name]

            # Prepare data for the map
            map_data = []
            if relevant_tracking_records:
                st.subheader("Tracking Records")
                tracking_df = pd.DataFrame(relevant_tracking_records)
                st.dataframe(tracking_df[['timestamp', 'location_name', 'count']])

                # Add tracking data to map_data
                for record in relevant_tracking_records:
                    map_data.append({
                        'latitude': record['latitude'],
                        'longitude': record['longitude'],
                        'description': f"Tracking Record: {record['timestamp']} at {record['location_name']}"
                    })

                    environmental_factors = get_environmental_factors(record['tracking_id'])
                    if environmental_factors:
                        st.write(f"**Environmental Factors for location :- {record['location_name']}:**")
                        for factor in environmental_factors:
                            st.write(f"- **{factor['factor_name']}:** {factor['factor_value']}")  # Display the factor name and its value
                    else:
                        st.write("No environmental factors found for this tracking ID.")

                # Fetch pollution data
                pollution_data = get_pollution_data(relevant_tracking_records[0]['location_id']) if relevant_tracking_records else []
                for pollution in pollution_data:
                    map_data.append({
                        'latitude': pollution['latitude'],
                        'longitude': pollution['longitude'],
                        'description': f"Pollution Source: {pollution['pollution_source_name']}, Type: {pollution['pollution_type']}, Level: {pollution['pollutant_level']}"
                    })

                # Create a Pydeck map
                if map_data:
                    st.subheader("Map Visualization")
                    deck = pdk.Deck(
                        initial_view_state=pdk.ViewState(
                            latitude=map_data[0]['latitude'],
                            longitude=map_data[0]['longitude'],
                            zoom=5,
                            pitch=0,
                        ),
                        layers=[
                            pdk.Layer(
                                "ScatterplotLayer",
                                data=map_data,
                                get_position=["longitude", "latitude"],
                                get_color=[255, 255, 0, 160],  # Red for tracking records
                                get_radius=25000,
                                pickable=True,
                                tooltip={
                                    "html": "<b>{description}</b>",
                                    "style": {
                                        "color": "white",
                                        "backgroundColor": "rgba(0, 0, 0, 0.7)",
                                        "border": "1px solid black",
                                        "borderRadius": "5px",
                                        "padding": "5px",
                                    },
                                },
                            )
                        ]
                    )
                    st.pydeck_chart(deck)

            else:
                st.write("No tracking records found for this species.")
        else:
            st.error("Species data not found.")
    else:
        st.write("No species found matching your query.")
else:
    st.warning("Please enter a species name to search.")            

#             if relevant_tracking_records:
#                 st.subheader("Tracking Records")
#                 tracking_df = pd.DataFrame(relevant_tracking_records)
#                 st.dataframe(tracking_df[['timestamp', 'location_name']])

#                 # Fetch location data
#                 location_data = get_location_data()
#                 for record in relevant_tracking_records:
#                     location_id = record['location_id']
#                     pollution_data = get_pollution_data(location_id)

#                     if pollution_data:
#                         st.write(f"**Pollution Sources in Location ID {location_id}:**")
#                         for pollution in pollution_data:
#                             st.write(f"- **Source Name:** {pollution['pollution_source_name']}, **Type:** {pollution['pollution_type']}, **Level:** {pollution['pollutant_level']}")

#             else:
#                 st.write("No tracking records found for this species.")
#         else:
#             st.error("Species data not found.")
#     else:
#         st.write("No species found matching your query.")
# else:
#     st.warning("Please enter a species name to search.")

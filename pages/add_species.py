import streamlit as st
from service.species_service import add_species
from service.habitat_service import add_habitat
from service.threat_service import add_threat
from service.migration_pattern_service import add_migration_pattern
from utils.fetch_images import fetch_images_from_unsplash


st.header("Add New Species")

# Input fields
common_name = st.text_input("Common Name")
scientific_name = st.text_input("Scientific Name")
conservation_status = st.selectbox("Conservation Status", ['Endangered', 'Vulnerable', 'Least Concern', 'Extinct'])
category = st.selectbox("Category", ['Fauna', 'Flora'])

# Input fields for habitat
habitat_type = st.text_input("Habitat Type")
habitat_description = st.text_area("Habitat Description")

# Input fields for migration pattern
migration_description = st.text_area("Migration Pattern Description")


# Input fields for threat description
threat_description = st.text_area("Threat description")
# Input fields for threat level
threat_level = st.slider("Threat Level", min_value=1, max_value=10, 
                         step=1, format="%.0f", 
                         key="threat_slider")

# Define the categories based on the ranges
if threat_level in [1, 2]:
    threat_label = "Very Low"
elif threat_level in [3, 4]:
    threat_label = "Low"
elif threat_level in [5, 6, 7]:
    threat_label = "Moderate"
elif threat_level == 8:
    threat_label = "High"
else:  # threat_level in [9, 10]
    threat_label = "Very High"

st.write(f"Threat level is {threat_label} ({threat_level})")



# Image selection
image_url = None
image_uploaded = st.file_uploader("Upload Image (Optional)", type=["jpg", "jpeg", "png"])

if not image_uploaded:
    fetch_images = st.checkbox("Fetch Images from Unsplash (Optional)")
    if fetch_images and common_name:
        image_urls = fetch_images_from_unsplash(common_name)
        if image_urls:
            st.write("Select one of the following images:")
            image_url = st.radio("Select Image", image_urls, format_func=lambda x: f"Image {image_urls.index(x) + 1}")
            st.image(image_url, caption="Selected Image", use_column_width=True)
else:
    image_url = image_uploaded.name

# Add species to database
if st.button("Submit"):
    if common_name and scientific_name and image_url and habitat_type:
        
        result = add_species(common_name, scientific_name, conservation_status, category, image_url)

        # Check if the result is a valid species ID or an error message
        if isinstance(result, int):  # Valid species ID
            # Add habitat
            add_habitat(habitat_type, habitat_description, result)

            # Add threat information
            if threat_description and threat_level:
                add_threat(threat_description, threat_level, result)

            # Add migration pattern information
            if migration_description:
                add_migration_pattern(migration_description, result)

        # add_habitat(habitat_type, habitat_description, new_species_id)

        # # Add threat information
        # if threat_description and threat_level:
        #     add_threat(threat_description, threat_level, new_species_id)

        # # Add migration pattern information
        # if migration_description:
        #     add_migration_pattern(migration_description, new_species_id)
            st.success(f"Species '{common_name}' and Habitat '{habitat_type}', Threat, and Migration Pattern added successfully!")

        else:
            st.error(result)

    else:
        st.error("Please fill in all required fields (Common Name, Scientific Name, Image, and Habitat Type).")

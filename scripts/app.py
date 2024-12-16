import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from datetime import datetime, timedelta

# Services
from service.species_service import add_species, get_species_data
from service.tracking_record_service import add_tracking_record, get_tracking_data
from service.location_service import add_location, get_location_data
from service.conservation_project_service import add_conservation_project
from service.pollution_source_service import add_pollution_source, get_pollution_sources
from service.research_study_service import add_research_study
import folium
from folium.plugins import HeatMap
from streamlit.components.v1 import html

# Selenium for web scraping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Geopy for geolocation
from geopy.geocoders import Nominatim
import time


today = datetime.today()
min_date = today - timedelta(days=365 * 100)
geolocator = Nominatim(user_agent="marine_biodiversity_tracking_system")


def fetch_images_from_unsplash(species_name):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') 
    options.add_argument('--no-sandbox') 

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = f'https://unsplash.com/s/photos/{species_name.replace(" ", "-")}'
    
    driver.get(url)
    
    time.sleep(5)
    
    images = driver.find_elements(By.TAG_NAME, "img")
    
    image_urls = []
    for img in images:
        img_url = img.get_attribute("src")
        if img_url:
            image_urls.append(img_url)
    
    # Close the browser
    driver.quit()
    
    return image_urls[:4]

st.title("Marine Biodiversity Tracking System")
background_image_path = "https://img.freepik.com/premium-photo/marine-marvel-underwater-landscape-ocean-life-oceanic-wonderland-exploring-marine-life-underwater-scenery-undersea-delight-ocean-view-marine-life-underwater-world-ai-generated_768733-52550.jpg?w=2000"
# st.markdown(f"""
#     <style>
#         .stApp {{
#             background-image: url("{background_image_path}");
#             background-size: cover;
#             background-position: center center;
#             background-repeat: no-repeat;
#             height: 100vh;
#             color: white;  /* Set text color to white for better contrast */
#         }}
#         .streamlit-expanderHeader {{
#             background-color: rgba(0, 0, 0, 0.3) !important;  /* Add a semi-transparent background to header */
#             color: white !important;  /* Ensure text is still readable */
#         }}
#         .stHeader, .stSubheader {{
#             background-color: rgba(0, 0, 0, 0.3) !important;  /* Add a semi-transparent background to headers */
#             padding: 10px;
#             border-radius: 5px;
#         }}
#         .stTextInput, .stSelectbox, .stTextArea {{
#             background-color: rgba(0, 0, 0, 0.5) !important;  /* Darker background for input fields */
#             color: white !important;  /* White text color for better visibility */
#             border-radius: 5px;
#         }}
#         .stButton {{
#             background-color: rgba(0, 0, 0, 0.7) !important;  /* Dark background for buttons */
#             color: white !important;  /* White text color for buttons */
#             border-radius: 5px;
#         }}
#         .stMarkdown {{
#             background-color: rgba(0, 0, 0, 0.5) !important;  /* Dark background for markdown */
#             padding: 15px;
#             border-radius: 5px;
#         }}
#     </style>
# """, unsafe_allow_html=True)


page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("{background_image_path}");
        background-size: 180%;
        background-position: top left;
        background-repeat: repeat;
        background-attachment: local;
        opacity: 1
        }}
    data-testid="stSidebar"] > div:first-child {{
        background-image: url("{background_image_path}");
        background-position: center; 
        background-repeat: no-repeat;
        background-attachment: fixed;
        }}

    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}

    [data-testid="stToolbar"] {{
        right: 2rem;
        }}
    </style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# tab = st.sidebar.radio("Choose functionality", ["Add Species", "Add Tracking Record", "View Data", "Visualize Data"])

tab = st.sidebar.radio(
    "Choose functionality",
    [
        "Add Species", "Add Tracking Record", "View Data", "Visualize Data",
        "Manage Locations", "Manage Conservation Projects", "Research Studies", 
        "Pollution Sources", "Visualize pollution sources"
    ]
)


# --- Add Species record ---
if tab == "Add Species":
    st.header("Add New Species")
    
    common_name = st.text_input("Common Name")
    scientific_name = st.text_input("Scientific Name")
    conservation_status = st.selectbox("Conservation Status", ['Endangered', 'Vulnerable', 'Least Concern', 'Extinct'])
    category = st.selectbox("Category", ['Fauna', 'Flora'])  # Added category input
    
    # Image upload or fetch options
    image_uploaded = st.file_uploader("Upload Image (Optional)", type=["jpg", "jpeg", "png"])
    
    # Initialize image_url as None
    image_url = None
    
    # If no image uploaded, allow fetching from Unsplash
    if not image_uploaded:
        fetch_images = st.checkbox("Fetch Images from Unsplash (Optional)")
        if fetch_images and common_name:
            image_urls = fetch_images_from_unsplash(common_name)
            if image_urls:
                st.write("Select one of the following images:")
                # Display fetched images as options
                image_url = st.radio("Select Image", image_urls, format_func=lambda x: f"Image {image_urls.index(x) + 1}")
                st.image(image_url, caption="Selected Image", use_column_width=True)
            else:
                st.warning("No images found on Unsplash for the given species.")
        elif not fetch_images:
            st.warning("Please check 'Fetch Images from Unsplash' to load images.")
    
    else:
        # If an image is uploaded, use that
        image_url = image_uploaded.name
    
    # Submit button to add the species to the database
    if st.button("Submit"):
        if common_name and scientific_name and image_url:
            # Call the function to add species, passing all the details including image URL
            add_species(common_name, scientific_name, conservation_status, category, image_url)
            st.success(f"Species '{common_name}' added successfully!")
        else:
            st.error("Please fill in all required fields (Common Name, Scientific Name, and select an image).")


# --- Add Tracking Record ---
elif tab == "Add Tracking Record":
    st.header("Add Tracking Record")
    species_data = get_species_data()  # Get species data (common_name, scientific_name, species_id)
    
    if not species_data:
        st.error("No species data available!")
    else:
        species_options = [f"{s['species_name']} ({s['scientific_name']})" for s in species_data]
        species_id = st.selectbox("Species", species_options)
        
        if species_id:
            selected_species_name = species_id.split(' (')[0]
            species_selected = next(s['species_id'] for s in species_data if s['species_name'] == selected_species_name)
            
            location_id = st.number_input("Location ID", min_value=1, step=1)
            timestamp = st.date_input("Date of Observation", value=datetime.today(), min_value=min_date)
            
            if st.button("Submit Record"):
                add_tracking_record(species_selected, location_id, timestamp)
                st.success(f"Tracking record for species '{species_id}' added successfully!")
        else:
            st.warning("Please select a species before submitting.")

# --- View Data ---
elif tab == "View Data":
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
        # st.dataframe(species_df)

    tracking_data = get_tracking_data()
    if tracking_data:
        # Display tracking data, ensuring we have species_id and related species information
        tracking_df = pd.DataFrame(tracking_data)
        tracking_df = tracking_df[['timestamp', 'species_id', 'location_id']]
        
        # Join with species data to display common_name and scientific_name alongside tracking data
        tracking_df = tracking_df.merge(species_df, how='left', left_on='species_id', right_on='id')
        tracking_df = tracking_df[['timestamp', 'species_id', 'species_name', 'scientific_name', 'location_id']]
        
        st.subheader("Tracking Data")
        st.dataframe(tracking_df)

# --- Visualize Data ---
elif tab == "Visualize Data":
    st.header("Data Visualization")
    
    tracking_data = get_tracking_data()
    if tracking_data:
        df = pd.DataFrame(tracking_data)
        
        # Merge tracking data with species information
        species_data = get_species_data()
        species_df = pd.DataFrame(species_data)
        
        df = df.merge(species_df, how='left', left_on='species_id', right_on='id')
        
        # Create the visualization: Line chart by species sightings over time
        fig = px.line(df, x='timestamp', y='common_name', title="Species Sightings Over Time", 
                      labels={'timestamp': 'Date', 'common_name': 'Species Name'})
        st.plotly_chart(fig)

# --- Manage Locations ---
elif tab == "Manage Locations":
    if 'locations' not in st.session_state:
        st.session_state.locations = []

    if 'coordinates' not in st.session_state:
        st.session_state.coordinates = [15.0, 20.0]  # Default coordinates

    # Inputs for the location name, latitude, longitude, and ecosystem type
    location_name = st.text_input("Location Name")
    latitude = st.number_input("Latitude", format="%.6f", value=st.session_state.coordinates[0], min_value=-90.0, max_value=90.0)
    longitude = st.number_input("Longitude", format="%.6f", value=st.session_state.coordinates[1], min_value=-180.0, max_value=180.0)
    ecosystem_type = st.selectbox("Ecosystem Type", ["Coral Reef", "Open Ocean", "Mangrove", "Estuary"])

    # Streamlit header
    st.header("Manage Locations")

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


# --- Manage Conservation Projects ---
elif tab == "Manage Conservation Projects":
    st.header("Manage Conservation Projects")
    
    # Conservation project entry fields
    project_name = st.text_input("Project Name")
    description = st.text_area("Project Description")
    start_date = st.date_input("Start Date", value=today)
    end_date = st.date_input("End Date", value=today + timedelta(days=365))
    organization_name = st.text_input("Organization Name")

    # Submit button to add conservation project
    if st.button("Add Conservation Project"):
        if project_name and organization_name:
            # Assuming a function add_conservation_project exists in service layer
            add_conservation_project(project_name, description, start_date, end_date, organization_name)
            st.success(f"Conservation Project '{project_name}' added successfully!")
        else:
            st.error("Please provide both project name and organization.")

# --- Research Studies ---
elif tab == "Research Studies":
    st.header("Manage Research Studies")
    
    # Research study entry fields
    study_title = st.text_input("Study Title")
    lead_researcher = st.text_input("Lead Researcher Name")
    species_focus = st.multiselect("Species Involved", [s['species_name'] for s in get_species_data()])

    # Submit button to add research study
    if st.button("Add Research Study"):
        if study_title and lead_researcher and species_focus:
            # Assuming a function add_research_study exists in service layer
            add_research_study(study_title, lead_researcher, species_focus)
            st.success(f"Research Study '{study_title}' added successfully!")
        else:
            st.error("Please provide study title, lead researcher, and select species.")

# --- Pollution Sources ---
elif tab == "Pollution Sources":
    st.header("Manage Pollution Sources")
    
    # Pollution source entry fields
    pollution_source_name = st.text_input("Pollution Source Name")
    pollution_type_options = ["Industrial Waste", "Agricultural Runoff", "Plastic Debris", "Chemical Spill", "Other"]
    pollution_type = st.selectbox("Pollution Type", pollution_type_options)
    
    # If the user selects "Other", allow manual input
    if pollution_type == "Other":
        pollution_type = st.text_input("Please specify the Pollution Type")
    pollutant_level = st.number_input("Pollutant Level", min_value=0.0, value=0.0, step=0.1)


    location_data = get_location_data()
    
    if location_data:
        # Display location options if data is available
        location_options = {l['location_name']: l['location_id'] for l in location_data}
        location_name = st.selectbox("Location Affected", list(location_options.keys()))
        location_id = location_options[location_name]
    else:
        # Allow user to manually enter a location if no data is available
        location_name = st.text_input("Location Name (No locations available in the database)")
        location_id = None  # No location ID for manually entered location

    # Submit button to add pollution source
    if st.button("Add Pollution Source"):
        if pollution_source_name and location_name:
            if location_id is None:
                # If location is manually entered, add it first
                add_location(location_name)  # Ensure you have a function to add the new location
                location_data = get_location_data()  # Re-fetch location data
                location_id = location_data[-1].id  # Assuming the new location is the last added
                
            # Add the pollution source with location_id
            add_pollution_source(pollution_source_name, pollution_type, location_id, pollutant_level)
            st.success(f"Pollution Source '{pollution_source_name}' added successfully!")
        else:
            st.error("Please provide pollution source name and location.")

elif tab == "Visualize pollution sources":
    
    st.subheader("Pollution Sources Heatmap")
    
    pollution_sources = get_pollution_sources()

    m = folium.Map(location=[0, 0], zoom_start=1)

    # Prepare heatmap data
    heatmap_data = []
    for source in pollution_sources:
        if source['latitude'] and source['longitude']:
            heatmap_data.append([source['latitude'], source['longitude'], source['pollutant_level']])

    # Add heatmap layer to the map
    if len(heatmap_data) > 0:
        HeatMap(heatmap_data, max_zoom=2).add_to(m)

    # Save the map to an HTML file
    map_html_path = 'pollution_sources_map.html'
    m.save(map_html_path)

    # Embed the map in the Streamlit app
    with open(map_html_path, 'r') as map_file:
        map_html = map_file.read()

    # Display the map
    html(map_html, height=600)

import streamlit as st
from utils.custom_styles import apply_custom_styles
from service.user_service import validate_user

# Set page configuration to hide sidebar by default (must be at the top)
st.set_page_config(page_title="Marine Biodiversity", layout="wide")

# Apply background and custom styles
# apply_custom_styles("https://img.freepik.com/premium-photo/marine-marvel-underwater-landscape-ocean-life-oceanic-wonderland-exploring-marine-life-underwater-scenery-undersea-delight-ocean-view-marine-life-underwater-world-ai-generated_768733-52550.jpg?w=2000")
apply_custom_styles("")

# Function to handle login logic
def handle_login():
    # Check if the user is already logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Show login form if the user is not logged in
    if not st.session_state.logged_in:
        st.title("Login to Access the App")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Hardcoded credentials (for simplicity, replace with secure method)
        # correct_username = "admin"
        # correct_password = "password123"

        if st.button("Login"):
            user = validate_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user.username
                st.session_state.role = user.role
                st.success(f"Login successful! Welcome, {user.role}.")
                st.session_state.show_sidebar = True
            else:
                st.error("Invalid username or password!")

# Function to handle logout
def handle_logout():
    # Ensure logout button only renders once for the session
    if "logged_in" in st.session_state and st.session_state.logged_in:
        if st.button("Logout", key="logout_button"):
            st.session_state.logged_in = False
            st.session_state.show_sidebar = False  # Hide the sidebar again after logout
            st.success("You have logged out.")

# Main application logic (only visible if logged in)
if "logged_in" in st.session_state and st.session_state.logged_in:
    # Show the logout button once across the app
    handle_logout()

    # Define pages for each feature (only accessible after login)
    species_page = st.Page("pages/add_species.py", title="Add Species", icon="🐟")
    tracking_page = st.Page("pages/add_tracking_record.py", title="Add Tracking Record", icon="📍")
    view_data_page = st.Page("pages/view_data.py", title="View Data", icon="📊")
    visualize_data_page = st.Page("pages/visualize_data.py", title="Visualize Data", icon="📈")
    locations_page = st.Page("pages/manage_locations.py", title="Manage Locations", icon="🌍")
    conservation_page = st.Page("pages/manage_conservation_projects.py", title="Manage Conservation Projects", icon="🌱")
    research_page = st.Page("pages/research_studies.py", title="Research Studies", icon="📚")
    pollution_page = st.Page("pages/pollution_sources.py", title="Pollution Sources", icon="💧")
    visualize_pollution_page = st.Page("pages/visualize_pollution.py", title="Visualize Pollution Sources", icon="🌐")
    view_species_details_page = st.Page("pages/view_species_details.py", title="View Species Details", icon="🐠")
    bulk_upload_page = st.Page("pages/bulk_upload.py", title="Bulk Upload", icon="📂")

    

    
    # st.header("Navigation")
    # st.markdown("### Select a page")

    # Show the sidebar after login
    if st.session_state.show_sidebar:
        if st.session_state.role == "Marine Biologist":
            allowed_pages = ["Add Species", "Bulk Upload", "View Data"]
        elif st.session_state.role == "Environmental Agency":
            allowed_pages = ["View Data", "View Species Details"]
        elif st.session_state.role == "Research Institution":
            allowed_pages = ["View Data", "Pollution Sources", "Manage Locations"]
        elif st.session_state.role == "Admin":
            allowed_pages = ["Bulk Upload",  "View Data", "View Species Details", "Add Species", "Manage Locations"]  # Admins can do everything
        else:
            allowed_pages = []

        pg = st.navigation({
            "Biodiversity": [species_page, tracking_page] if "Add Species" in allowed_pages or "Add Tracking Record" in allowed_pages else [],
            "Data": [view_data_page, visualize_data_page] if "View Data" in allowed_pages else [],
            "Management": [locations_page, conservation_page, research_page] if "Manage Locations" in allowed_pages else [],
            "Environmental Impact": [pollution_page, visualize_pollution_page] if "Pollution Sources" in allowed_pages else [],
            "View Species Details": [view_species_details_page] if "View Species Details" in allowed_pages else [],
            "Upload": [bulk_upload_page] if "Bulk Upload" in allowed_pages else [],
        })
        pg.run()

else:
    # If not logged in, just show the login screen
    handle_login()

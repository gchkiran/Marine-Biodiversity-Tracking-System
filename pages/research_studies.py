import streamlit as st
from service.research_study_service import add_research_study
from service.species_service import get_species_data


st.header("Manage Research Studies")

study_title = st.text_input("Study Title")
lead_researcher = st.text_input("Lead Researcher Name")
species_focus = st.multiselect("Species Involved", [s['species_name'] for s in get_species_data()])

if st.button("Add Research Study"):
    if study_title and lead_researcher and species_focus:
        add_research_study(study_title, lead_researcher, species_focus)
        st.success(f"Research Study '{study_title}' added successfully!")

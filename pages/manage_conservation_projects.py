import streamlit as st
from service.conservation_project_service import add_conservation_project
from datetime import datetime, timedelta

today = datetime.today()

st.header("Manage Conservation Projects")

project_name = st.text_input("Project Name")
description = st.text_area("Project Description")
start_date = st.date_input("Start Date", value=today)
end_date = st.date_input("End Date", value=today + timedelta(days=365))
organization_name = st.text_input("Organization Name")

if st.button("Add Conservation Project"):
    if project_name and organization_name:
        add_conservation_project(project_name, description, start_date, end_date, organization_name)
        st.success(f"Conservation Project '{project_name}' added successfully!")

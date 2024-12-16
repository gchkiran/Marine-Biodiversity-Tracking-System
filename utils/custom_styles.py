import streamlit as st

def apply_custom_styles(background_image_url):
    st.markdown(
        f"""
       <style>
       [data-testid="stAppViewContainer"] > .main {{
            background-image: url("{background_image_url}");
            background-size: 180%;
            background-position: top left;
            background-repeat: repeat;
            background-attachment: local;
            opacity: 1
        }}
        data-testid="stSidebar"] > div:first-child {{
            background-image: url("{background_image_url}");
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
        """,
        unsafe_allow_html=True
    )

import streamlit as st
import pandas as pd
import numpy as np
from service.species_service import add_species
from service.habitat_service import add_habitat
from service.threat_service import add_threat
from service.migration_pattern_service import add_migration_pattern

st.header("Bulk Upload Species Data")

# File upload
uploaded_file = st.file_uploader("Upload CSV/Excel File", type=["csv", "xlsx"])

if uploaded_file:
    # Load the data
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head(10))  # Show a preview of the data

        # Validate the required columns
        required_columns = ['common_name', 'scientific_name', 'conservation_status', 
                            'category', 'habitat_type', 'habitat_description', 
                            'threat_description', 'threat_level', 'migration_description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
        else:
            if st.button("Submit to Database"):
                df = df.replace({np.nan: None})
                total_rows = len(df)
                
                # Add a progress bar
                progress_bar = st.progress(0)
                progress_text = st.empty()
                
                for index, row in df.iterrows():
                    try:
                        # Add species
                        result = add_species(
                            row['common_name'],
                            row['scientific_name'],
                            row['conservation_status'],
                            row['category'],
                            row.get('image_url', None)
                        )

                        # Check if the result is a valid species ID or an error message
                        if isinstance(result, int):  # Valid species ID
                            # Add habitat
                            add_habitat(
                                row['habitat_type'],
                                row['habitat_description'],
                                result
                            )

                            # Add threat
                            if pd.notna(row['threat_description']) and pd.notna(row['threat_level']):
                                add_threat(
                                    row['threat_description'],
                                    int(row['threat_level']),
                                    result
                                )

                            # Add migration pattern
                            if pd.notna(row['migration_description']):
                                add_migration_pattern(
                                    row['migration_description'],
                                    result
                                )
                        else:
                            st.error(f"Error for row {index + 1}: {result}")

                    except Exception as e:
                        st.error(f"Error processing row {index + 1}: {e}")
                    
                    # Update progress bar and text
                    progress = (index + 1) / total_rows
                    progress_bar.progress(progress)
                    progress_text.text(f"Processing row {index + 1} of {total_rows}")

                progress_text.text("Upload completed!")
                st.success("All species data has been successfully added to database!")

    except Exception as e:
        st.error(f"An error occurred: {e}")

import pandas as pd

# Sample data for the Excel file
data = {
    "common_name": ["Dolphin", "Blue Whale", "Sea Turtle", "Shark", "Coral"],
    "scientific_name": [
        "Delphinus delphis",
        "Balaenoptera musculus",
        "Chelonia mydas",
        "Carcharodon carcharias",
        "Acropora cervicornis"
    ],
    "conservation_status": ["Vulnerable", "Endangered", "Endangered", "Vulnerable", "Critically Endangered"],
    "category": ["Fauna", "Fauna", "Fauna", "Fauna", "Flora"],
    "habitat_type": ["Ocean", "Ocean", "Coastal Waters", "Ocean", "Coral Reef"],
    "habitat_description": [
        "Deep waters",
        "Large deep waters",
        "Shallow coastal waters",
        "Wide-ranging predator",
        "Coral reef ecosystems"
    ],
    "threat_description": [
        "Overfishing",
        "Ship strikes",
        "Plastic pollution",
        "Bycatch",
        "Coral bleaching"
    ],
    "threat_level": [8, 9, 7, 6, 10],
    "migration_description": [
        "Seasonal migration",
        "Long-distance migration",
        "Coastal migration",
        "Wide-ranging movement",
        "Stationary"
    ],
    "image_url": ["", "", "", "", ""]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame as an Excel file
file_path = "sample_species_data.xlsx"
df.to_excel(file_path, index=False)

print(f"Excel file saved as {file_path}")

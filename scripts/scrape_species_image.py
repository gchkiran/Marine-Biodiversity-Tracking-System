import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


# Function to fetch image URLs from Unsplash for a species
def fetch_images_from_unsplash(species_name):
    # Set up Selenium to use Chrome
    options = Options()
    options.add_argument('--headless')  # Run in headless mode (without opening a browser window)
    options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
    options.add_argument('--no-sandbox')  # To avoid issues in certain environments

    # Set up the webdriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Construct the Unsplash search URL
    url = f'https://unsplash.com/s/photos/{species_name.replace(" ", "-")}'
    
    # Open the page
    driver.get(url)
    
    # Wait for the page to load completely (adjust time if needed)
    time.sleep(5)
    
    # Find all image elements on the page
    images = driver.find_elements(By.TAG_NAME, "img")
    
    # Extract URLs from the 'src' attribute of each image
    image_urls = []
    for img in images:
        img_url = img.get_attribute("src")
        if img_url:
            image_urls.append(img_url)
    
    # Close the browser
    driver.quit()
    
    return image_urls

# Function to update the image URLs in the database
def update_species_images(db_config):
    # Connect to the MySQL database using the provided configuration (username, password, etc.)
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Fetch all species names from the table (assuming the table is named 'species')
    cursor.execute("SELECT id, common_name FROM species")
    species_rows = cursor.fetchall()
    
    # For each species, fetch image URLs and update the database
    for species_id, species_name in species_rows:
        print(f"Processing species: {species_name}")
        
        # Fetch images from Unsplash for the species
        image_urls = fetch_images_from_unsplash(species_name)
        
        # If image URLs were found, update the database
        if image_urls:
            # Use the first image URL as the `image_url` (you can modify this logic)
            image_url = image_urls[0]  # You can modify this if you want to store multiple URLs or choose differently
            
            # Update the species record in the database with the first image URL
            cursor.execute("UPDATE species SET image_url = %s WHERE id = %s", (image_url, species_id))
            conn.commit()
            print(f"Updated image URL for {species_name}: {image_url}")
        else:
            print(f"No images found for {species_name}")
    
    # Close the database connection
    conn.close()

# MySQL database configuration
db_config = {
    'host': 'localhost',  # Your MySQL server host, usually 'localhost'
    'user': 'username',  # Replace with your MySQL username
    'password': 'password',  # Replace with your MySQL password
    'database': 'dbname',  # Replace with your database name
    'port': 3306  # Default MySQL port (change if different)
}

# Call the function with the database configuration
update_species_images(db_config)

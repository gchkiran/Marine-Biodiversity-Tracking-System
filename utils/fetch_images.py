from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_images_from_unsplash(species_name):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f'https://unsplash.com/s/photos/{species_name.replace(" ", "-")}'
    driver.get(url)
    time.sleep(0.2)

    images = driver.find_elements(By.TAG_NAME, "img")
    image_urls = [img.get_attribute("src") for img in images if img.get_attribute("src")]
    driver.quit()
    return image_urls[:4]

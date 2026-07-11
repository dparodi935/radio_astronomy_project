from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

link =  "https://lofar-surveys.org/hd-en1.html"

options = Options()
#"headless" means the webpage isn't visibly opened
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage") #related to preventing memory crashes
#set download path
download_path = os.path.join('..','lofar_downloads')
if not os.path.isdir(download_path):
    os.mkdir(download_path)
download_path = os.path.abspath(download_path)

prefs = {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
}
options.add_experimental_option("prefs", prefs)


#driver is what allows us to interact with the webpage. 
driver = webdriver.Chrome(options=options)
driver.get(link)


number_entries_name = "table_id_length"

#find the dropdown table with the number of entries and set it to 50 so all entries are included
element = driver.find_element(By.NAME, number_entries_name)
dropdown_element = Select(element)
dropdown_element.select_by_value("50")

#select all the rows
rows = driver.find_elements(By.CSS_SELECTOR,"#table_id tbody tr")

data = []

for i, row in enumerate(rows):
    cells = row.find_elements(By.TAG_NAME, "td")
    #select column: 0 = 0.3-arcsec, 2 = 0.6-arcsec, 3 = 1.2-arcsec 4 = region files
    image, region = cells[3], cells[4]

    #clicks the download button
    button = image.find_element(By.TAG_NAME, "a")
    button.click()

    button = region.find_element(By.TAG_NAME, "a")
    button.click()

    print(f"Downloaded row {i+1}")

#this is so I can hold the connection open till the download is complete
input()
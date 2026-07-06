from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link =  "https://lofar-surveys.org/hd-en1.html"

#driver is what allows us to interact with the webpage
driver = webdriver.Firefox()
driver.get(link)

number_entries_name = "table_id_length"

#find the dropdown table with the number of entries and set it to 50 so all entries are included
element = driver.find_element(By.NAME,number_entries_name)
dropdown_element = Select(element)
dropdown_element.select_by_value("50")

#select all the rows
rows = driver.find_elements(By.CSS_SELECTOR,"#table_id tbody tr")

data = []

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")

    cell = cells[3]

    button = cell.find_element(By.TAG_NAME, "a")
    button.click()

print(data)
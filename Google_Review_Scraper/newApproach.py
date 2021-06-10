from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException
import time 
import string
import openpyxl
import os


#Loading Selenium Webdriver 
driver= webdriver.Chrome()
wait = WebDriverWait(driver, 5)
 
#Opening Google maps 
driver.get("https://www.google.com/maps")
time.sleep(3)

#Finding the search box 
driver.switch_to_default_content()
searchbox=driver.find_element_by_id('searchboxinput')
location= "MAXBURST, Inc., Broadhollow Road #12e, Farmingdale, NY, USA"
searchbox.send_keys(location)
searchbox.send_keys(Keys.ENTER)
time.sleep(2)

expand = driver.find_element_by_class_name("widget-pane-link")
expand.click()

review_title = driver.find_element_by_class_name("section-review-title")
review_title.text


# cancelbut.click()
# searchbox.send_keys("seguro")
# searchbox.send_keys(Keys.ENTER)
# time.sleep(3)

# #Locating the results section 
# entries=driver.find_elements_by_class_name('section-result')


# #Prepare the excel file using the Openpyxl  
# wb= openpyxl.load_workbook("comapnies.xlsx")
# sheetname=wb.get_sheet_names()[0]
# sheet=wb[sheetname]
# sheet.title ="companies"
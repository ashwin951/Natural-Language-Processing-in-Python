from logging import exception
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


class WebDriver:
    location_data = {}
    def __init__(self):
        self.driver= webdriver.Chrome()
        wait = WebDriverWait(self.driver, 5)
 
        #Opening Google maps 
        self.driver.get("https://www.google.com/maps")
        time.sleep(3)

        self.location_data["rating"] = "NA"
        self.location_data["reviews_count"] = "NA"
        self.location_data["location"] = "NA"
        self.location_data["contact"] = "NA"
        self.location_data["website"] = "NA"
        self.location_data["Time"] = {"Monday":"NA", "Tuesday":"NA", "Wednesday":"NA", "Thursday":"NA", "Friday":"NA", "Saturday":"NA", "Sunday":"NA"}
        self.location_data["Reviews"] = []
        self.location_data["Popular Times"] = {"Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[], "Sunday":[]}

    def click_all_reviews_button(self):
        
        try:
            time.sleep(4)
            expand = self.driver.find_element_by_class_name("widget-pane-link")
            self.location_data["reviews_count"] = int(expand.text.split(' ')[0])
            expand.click()
        except:
        
            self.driver.quit()
            return False
        return True
    
    
    def scroll_the_page(self):
        try:
    
    
            pause_time = 4 # Waiting time after each scroll.
            max_count = int(self.location_data["reviews_count"]/5) # Number of times we will scroll the scroll bar to the bottom.
            x = 0
    
            while(x<max_count):
                
                scrollable_div = self.driver.find_element_by_css_selector("div.section-layout.section-scrollbox.mapsConsumerUiCommonScrollable__scrollable-y.mapsConsumerUiCommonScrollable__scrollable-show") # It gets the section of the scroll bar.
                try:
                    
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div) # Scroll it to the bottom.
                except:
                    pass
                
                time.sleep(pause_time) # wait for more reviews to load.
                x=x+1

        except:
            self.driver.quit()
            pass
    def expand_all_reviews(self):
        try:
            element = self.driver.find_elements_by_class_name("mapsConsumerUiSubviewSectionReview__section-expand-review mapsConsumerUiCommonButton__blue-link")
            print('element',element)
            for i in element:
                i.click()
        except:
            print('expand all reviews error')
            pass
    def get_reviews_data(self):
    
        try:
            print('Step 1')
            # review_names = self.driver.find_elements_by_class_name("section-review-title") # Its a list of all the HTML sections with the reviewer name.
            review_names = self.driver.find_elements_by_class_name("ODSEW-ShBeI-title")
            print('Step 2')
            # review_text = self.driver.find_elements_by_class_name("mapsConsumerUiSubviewSectionReview__section-review-review-content") # Its a list of all the HTML sections with the reviewer reviews.
            review_text = self.driver.find_elements_by_class_name("ODSEW-ShBeI-text") # Its a list of all the HTML sections with the reviewer reviews. 
            print('Step 3')
            # review_dates = self.driver.find_elements_by_css_selector("[class='section-review-publish-date']") # Its a list of all the HTML sections with the reviewer reviewed date.
            review_dates = self.driver.find_elements_by_css_selector("[class='ODSEW-ShBeI-RgZmSc-date']") # Its a list of all the HTML sections with the reviewer reviewed date. 
            print('Step 4')
            # review_stars = self.driver.find_elements_by_css_selector("[class='section-review-stars']") # Its a list of all the HTML sections with the reviewer rating.
            review_stars = self.driver.find_elements_by_css_selector("[class='ODSEW-ShBeI-H1e3jb']") # Its a list of all the HTML sections with the reviewer rating.
            review_stars_final = []

            for i in review_stars:
                review_stars_final.append(i.get_attribute("aria-label"))

            review_names_list = [a.text for a in review_names]
            review_text_list = [a.text for a in review_text]
            review_dates_list = [a.text for a in review_dates]
            review_stars_list = [a for a in review_stars_final]


            for (a,b,c,d) in zip(review_names_list, review_text_list, review_dates_list, review_stars_list):
                self.location_data["Reviews"].append({"name":a, "review":b, "date":c, "rating":d})

        except Exception as e:
            print('error')
            pass

    def scrape(self, location): # Passed the URL as a variable
        try:

            self.driver.switch_to_default_content()
            searchbox=self.driver.find_element_by_id('searchboxinput')
            
            searchbox.send_keys(location)
            searchbox.send_keys(Keys.ENTER)
            

        except Exception as e:

            self.driver.quit()
            return

        time.sleep(10) # Waiting for the page to load.
        self.click_all_reviews_button()
        time.sleep(5) # Waiting for the all reviews page to load.
        self.scroll_the_page() # Scrolling the page to load all reviews.
        self.expand_all_reviews() # Expanding the long reviews by clicking see more button in each review.
        self.get_reviews_data() # Getting all the reviews data.
        self.driver.quit() # Closing the driver instance.
        return(self.location_data) # Returning the Scraped Data.


companyNameList = ['Vistas - Web Development, Web Design Company in Bangalore, SEO Digital Marketing Services Company, eCommerce Web Development in Bangalore']
for num in range(len(companyNameList)):
    location = companyNameList[num] 
    x = WebDriver()
    time.sleep(15)
    finalJSon = x.scrape(location)
    df = pd.DataFrame(finalJSon['Reviews'])
    print(df.head())
    df.to_csv('vistas.csv'.format(num),header=True,index=False)



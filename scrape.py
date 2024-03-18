from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import time as time
from utils import *


    
# Replace this with the path to your downloaded ChromeDriver
CHROME_DRIVER_PATH = '/Users/samfeldman/Downloads/chromedriver-mac-arm64/chromedriver'

driver = initialize_driver(CHROME_DRIVER_PATH)

PAGE_LINK = 'https://colleges.wearecollegetennis.com/Results/Completed?gender=MALE&division=DIVISION_1'
def scrape_results(driver, page_url):
  
    with initialize_driver(CHROME_DRIVER_PATH) as driver:
        driver.get(page_url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        click_cookie_button(driver)
        click_load_more(driver, 2)
        links = get_button_links(driver)
        main_df = pd.DataFrame()
        count = 0
        for link in links:
          try:
              df = scrape_box_score(driver, link)
              main_df = pd.concat([main_df, df], ignore_index=True)
              print(f"Scraped {count + 1} of {len(links)}")
              count += 1
          except:
              print(f"Error on {link}")
              continue
            
        return main_df


def main():
    start = time.time()
    

    results_df = scrape_results(CHROME_DRIVER_PATH, PAGE_LINK)
    results_df.to_excel('output.xlsx', index=False)
    end = time.time()
    
    print(f"Time elapsed: {end - start:.2f} seconds")

if __name__ == "__main__":
    main()
    # driver = initialize_driver(CHROME_DRIVER_PATH)
    # scrape_box_score(driver, 'https://colleges.wearecollegetennis.com/PrincetonUniversityM/Team/scorecard/168C826C-3C57-455C-9C45-A7624D749F2A')

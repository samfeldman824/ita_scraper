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
import json


    
# Replace this with the path to your downloaded ChromeDriver
CHROME_DRIVER_PATH = '/Users/samfeldman/Downloads/chromedriver-mac-arm64/chromedriver'

driver = initialize_driver(CHROME_DRIVER_PATH)

PAGE_LINK = 'https://colleges.wearecollegetennis.com/Results/Completed?gender=FEMALE&division=DIVISION_1'
def scrape_results(driver: webdriver.Chrome, page_url: str) -> pd.DataFrame:
  """
  Scrapes the results from a web page using the provided driver and page URL.

  Args:
    driver: The web driver used to interact with the web page.
    page_url: The URL of the web page to scrape.

  Returns:
    A pandas DataFrame containing the scraped data.

  Raises:
    Any exceptions that occur during the scraping process.
  """
  saved_names = {}

  with open('saved_names.json', 'r') as f:
    saved_names = json.load(f)

  print(f"len saved names: {len(saved_names)}")

  with initialize_driver(CHROME_DRIVER_PATH) as driver:
    driver.get(page_url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    click_cookie_button(driver)
    click_load_more(driver, 4)
    links = get_button_links(driver)
    main_df = pd.DataFrame()
    count = 0

    for link in links:
      if count == 10:
        break
      try:
        df = scrape_box_score(driver, link, saved_names)
        main_df = pd.concat([main_df, df], ignore_index=True)
        print(f"Scraped {count + 1} of {len(links)}")
        print(len(saved_names))
        count += 1
      except Exception as e:
        print(f"Error on {link}")
        print(e)
        continue

    print(f"len saved names: {len(saved_names)}")

    with open('saved_names.json', 'w') as f:
      json.dump(saved_names, f)

    return main_df


def main():
    start = time.time()
    

    results_df = scrape_results(CHROME_DRIVER_PATH, PAGE_LINK)
    results_df.to_excel('output.xlsx', index=False)
    end = time.time()
    
    print(f"Time elapsed: {end - start:.2f} seconds")

if __name__ == "__main__":
    main()
    # with open('saved_names.json', 'r') as f:
    #         saved_names = json.load(f)
    # driver = initialize_driver(CHROME_DRIVER_PATH)
    # scrape_box_score(driver, 'https://colleges.wearecollegetennis.com/vr?id=EEC765AE-0EAC-40F4-A2B6-749AFEDE93FE&a=Index&c=VenueTeam&s=/scorecard/AEE162B8-05F7-491E-9391-A5C5398EC642', saved_names)
# https://colleges.wearecollegetennis.com/vr?id=12DA963F-DB09-4430-8238-0C5972BD0AAE&a=Index&c=VenueTeam&s=/scorecard/E2FC0807-8A03-4B16-8CA9-0D03148651A9
# https://colleges.wearecollegetennis.com/vr?id=EEC765AE-0EAC-40F4-A2B6-749AFEDE93FE&a=Index&c=VenueTeam&s=/scorecard/AEE162B8-05F7-491E-9391-A5C5398EC642
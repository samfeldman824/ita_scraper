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
import requests
import random



    
# Replace this with the path to your downloaded ChromeDriver
CHROME_DRIVER_PATH = '/Users/samfeldman/Downloads/chromedriver-mac-arm64/chromedriver'

driver = initialize_driver(CHROME_DRIVER_PATH)
DIVISION = 'DIVISION_1'
GENDER = 'MALE'
CONFERENCE = 'Ivy_League'

# BASE_URL = 'https://colleges.wearecollegetennis.com/Results/Completed'
PAGE_LINK = f"https://colleges.wearecollegetennis.com/Results/Completed?division={DIVISION}&conference={CONFERENCE}&gender={GENDER}"
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

  

  with initialize_driver('/Users/samfeldman/Downloads/chromedriver-mac-arm64/chromedriver') as driver:
    driver.get(page_url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    click_cookie_button(driver)
    click_load_more(driver, 2)
    links = get_button_links(driver)
    main_df = pd.DataFrame()
    count = 0

    links = [
    # 'https://colleges.wearecollegetennis.com/vr?id=0CDD94A1-39FE-44AE-A9BC-CDB1A87D6F32&a=Index&c=VenueTeam&s=/scorecard/3000ED76-044E-4830-A62E-9B0874493CF5',
    # 'https://colleges.wearecollegetennis.com/vr?id=12DA963F-DB09-4430-8238-0C5972BD0AAE&a=Index&c=VenueTeam&s=/scorecard/E2FC0807-8A03-4B16-8CA9-0D03148651A9',
    # 'https://colleges.wearecollegetennis.com/vr?id=EEC765AE-0EAC-40F4-A2B6-749AFEDE93FE&a=Index&c=VenueTeam&s=/scorecard/AEE162B8-05F7-491E-9391-A5C5398EC642',
    # 'https://colleges.wearecollegetennis.com/vr?id=85B89882-F2B1-4BDC-A1F2-4CEE0C1AD6CD&a=Index&c=VenueTeam&s=/scorecard/32230C17-52D7-413E-A13B-137EF0A5B3B1',
    # 'https://colleges.wearecollegetennis.com/OldDominionUniversityM/Team/scorecard/CD56CA4B-69F6-4F81-B535-0A57D2412DB3'
    ]


    # proxy_file_path = 'valid_proxies.txt'
    # proxies = read_proxies_from_file(proxy_file_path)
  
    # counter = 0
    # proxy_length = len(proxies)

    user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    ]
    
    

    

    for link in links:
      
      agent = random.choice(user_agents)
      CHROME_DRIVER_PATH = '/Users/samfeldman/Downloads/chromedriver-mac-arm64/chromedriver'
      service = Service(executable_path=CHROME_DRIVER_PATH)
      options = webdriver.ChromeOptions()
      options.add_argument(f'user-agent={agent}')

      new_driver = webdriver.Chrome(service=service, options=options)
      
      # driver_proxy = create_driver_with_proxy(proxies[counter % proxy_length])
      
      # if count == -10:
      #   break
      try:
        df = scrape_box_score(new_driver, link, saved_names)
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
      json.dump(saved_names, f, indent=4)

    return main_df


def main():
    start = time.time()
    

    results_df = scrape_results(CHROME_DRIVER_PATH, PAGE_LINK)
    # results_df = scrape_results(CHROME_DRIVER_PATH, BASE_URL)
    results_df.to_excel('output.xlsx', index=False)
    end = time.time()
    
    print(f"Time elapsed: {end - start:.2f} seconds")

if __name__ == "__main__":
    main()
    # with open('saved_names.json', 'r') as f:
    #         saved_names = json.load(f)
    # driver = initialize_driver(CHROME_DRIVER_PATH)
    # scrape_box_score(driver, 'https://colleges.wearecollegetennis.com/vr?id=12DA963F-DB09-4430-8238-0C5972BD0AAE&a=Index&c=VenueTeam&s=/scorecard/E2FC0807-8A03-4B16-8CA9-0D03148651A9', saved_names)
# 
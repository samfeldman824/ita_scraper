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
import argparse
from icecream import ic

ic.configureOutput(prefix='')

config = read_config()

CHROME_DRIVER_PATH = config['Setup']['chrome_driver_path']

argparse = argparse.ArgumentParser()
argparse.add_argument('--division', '-d', type=str)
argparse.add_argument('--gender', '-g', type=str)
argparse.add_argument('--conference', '-c', type=str)

args = argparse.parse_args()

BASE_URL = 'https://colleges.wearecollegetennis.com/Results/Completed?'

url = BASE_URL

url_params = []

if args.division:
  url_params.append(f'division={division_dict[args.division]}')
if args.gender:
  if args.gender == 'm':
    url_params.append('gender=MALE')
  if args.gender == 'f':
    url_params.append('gender=FEMALE')
if args.conference:
  url_params.append(f'conference={args.conference}')

if url_params:
  url = BASE_URL + '&'.join(url_params)

PAGE_LINK = url
print()
# print(f"Scraping link: {PAGE_LINK}")
ic(PAGE_LINK)
# driver = initialize_driver(CHROME_DRIVER_PATH)

# service = Service(executable_path=CHROME_DRIVER_PATH)
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=service, options=options)
    


saved_names = {}

with open('saved_names.json', 'r') as f:
  saved_names = json.load(f)

num_names_start = len(saved_names)

ic(len(saved_names))

def scrape_results(driver_path: str, page_url: str, saved_names: dict) -> pd.DataFrame:
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
  

  

  with initialize_driver(driver_path) as driver:
    driver.get(page_url)
    driver.set_window_position(0, 0)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    click_cookie_button(driver)
    click_load_more(driver, 3)
    links = get_button_links(driver)
    main_df = pd.DataFrame()
    count = 1
    num_success = 0
    num_failed = 0
    # links = links[0:44]

    
    # links = [
      # 'https://colleges.wearecollegetennis.com/vr?id=C7CA88A5-8AC0-4476-9AF9-C93D9C2DD777&a=Index&c=VenueTeam&s=/scorecard/8917DFD2-0A98-4255-A7B8-540F544ABDD2',
      # 'https://colleges.wearecollegetennis.com/vr?id=C9CA8B99-867B-4C0F-A57E-3445EF22D5A6&a=Index&c=VenueTeam&s=/scorecard/8A58A946-BD9B-4DE7-BAF0-DF4D63D87A53'
    #   'https://colleges.wearecollegetennis.com/AmericanRiverCollegeW/Team/scorecard/42B30D0C-129B-423D-A26C-EE8933B679FE'
      # 'https://colleges.wearecollegetennis.com/DoaneUniversityM/Team/scorecard/AB9374DF-D627-424E-A44C-11744013465B'
      # 'https://colleges.wearecollegetennis.com/vr?id=C22FC68C-0780-446B-AD46-EB2C49901F5D&a=Index&c=VenueTeam&s=/scorecard/A89D820C-ED58-464F-A495-5F4B0A052E98',
    # 'https://colleges.wearecollegetennis.com/vr?id=0CDD94A1-39FE-44AE-A9BC-CDB1A87D6F32&a=Index&c=VenueTeam&s=/scorecard/3000ED76-044E-4830-A62E-9B0874493CF5',
    # 'https://colleges.wearecollegetennis.com/vr?id=12DA963F-DB09-4430-8238-0C5972BD0AAE&a=Index&c=VenueTeam&s=/scorecard/E2FC0807-8A03-4B16-8CA9-0D03148651A9',
    # 'https://colleges.wearecollegetennis.com/vr?id=EEC765AE-0EAC-40F4-A2B6-749AFEDE93FE&a=Index&c=VenueTeam&s=/scorecard/AEE162B8-05F7-491E-9391-A5C5398EC642',
    # 'https://colleges.wearecollegetennis.com/vr?id=85B89882-F2B1-4BDC-A1F2-4CEE0C1AD6CD&a=Index&c=VenueTeam&s=/scorecard/32230C17-52D7-413E-A13B-137EF0A5B3B1',
    # 'https://colleges.wearecollegetennis.com/OldDominionUniversityM/Team/scorecard/CD56CA4B-69F6-4F81-B535-0A57D2412DB3'
    # ]


    # proxy_file_path = 'valid_proxies.txt'
    # proxies = read_proxies_from_file(proxy_file_path)
  
    # counter = 0
    # proxy_length = len(proxies)

    user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    ]
    
    

    ic(len(links)) 
    
    error_links = []
    for link in links:
      
      # agent = random.choice(user_agents)
      # CHROME_DRIVER_PATH = '/Users/samfeldman/Downloads/chromedriver-mac-arm64/chromedriver'
      # service = Service(executable_path=CHROME_DRIVER_PATH)
      # options = webdriver.ChromeOptions()
      # options.add_argument(f'user-agent={agent}')

      # new_driver = webdriver.Chrome(service=service, options=options)
      
      # driver_proxy = create_driver_with_proxy(proxies[counter % proxy_length])
      
      # if count == -10:
      #   break
      print(f"Scraping {count} of {len(links)}")
      try:
        # df = scrape_box_score(new_driver, link, saved_names)
        df = scrape_box_score(driver, link, saved_names)
        main_df = pd.concat([main_df, df], ignore_index=True)
        print(f"Scraped {count} of {len(links)}")
        ic(len(saved_names))
        num_success += 1
        
      except Exception as e:
        print(f"Error on {link}")
        print(e)
        num_failed += 1
        error_links.append(link)
        continue
      
      finally:
        count += 1
    
    ic(len(saved_names))
    with open('saved_names.json', 'w') as f:
      json.dump(saved_names, f, indent=4)
    ic(num_success)
    ic(num_failed)
    # print(f"Success: {num_success}")
    # print(f"Failed: {num_failed}")
    if error_links:
      print("Failed Links:")
      for link in error_links:
        print(link)
      
    

    return main_df


def main():
  start = time.time()
  

  results_df = scrape_results(CHROME_DRIVER_PATH, PAGE_LINK, saved_names)
  results_df.to_excel('output.xlsx', index=False)
  end = time.time()
  
  num_names_end = len(saved_names)
  names_added = num_names_end - num_names_start
  ic(names_added)
  
  execution_time = "{:.2f}".format(end - start) + " seconds"
   
  ic(execution_time)

if __name__ == "__main__":
    main()
    # with open('saved_names.json', 'r') as f:
    #         saved_names = json.load(f)
    # driver = initialize_driver(CHROME_DRIVER_PATH)
    # scrape_box_score(driver, 'https://colleges.wearecollegetennis.com/vr?id=12DA963F-DB09-4430-8238-0C5972BD0AAE&a=Index&c=VenueTeam&s=/scorecard/E2FC0807-8A03-4B16-8CA9-0D03148651A9', saved_names)
# 
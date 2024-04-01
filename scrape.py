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

def parse_arguments():
    args = argparse.ArgumentParser()
    args.add_argument('--division', '-d', type=str)
    args.add_argument('--gender', '-g', type=str)
    args.add_argument('--conference', '-c', type=str)
    return args.parse_args()

def construct_url(args):
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
  
  return url

def load_saved_names():
  saved_names = {}
  with open('saved_names.json', 'r') as f:
    saved_names = json.load(f)
  return saved_names

def save_saved_names(saved_names):
  with open('saved_names.json', 'w') as f:
      json.dump(saved_names, f, indent=4)

def find_links(page_link, num_clicks):
  driver = initialize_driver()
  driver.get(page_link)
  WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
  click_cookie_button(driver)
  click_load_more(driver, num_clicks)
  links = get_button_links(driver)
  return links

def scrape_links(links: list, saved_names: dict):
  
  driver = initialize_driver()
  main_df = pd.DataFrame()
  count = 1
  num_success = 0
  num_failed = 0
  error_links = []
  len_names_start = len(saved_names)
  
  for link in links:
    try:
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

  save_saved_names(saved_names)
  
  if error_links:
      print("Failed Links:")
      for link in error_links:
        print(link) 

  names_added = len(saved_names) - len_names_start


  ic(num_success)
  ic(num_failed)
  ic(names_added)

  return main_df



def main():
  config = read_config()
  args = parse_arguments()
  page_url = construct_url(args)
  saved_names = load_saved_names()
  links = find_links(page_url, 1)[0:10]
      
  start = time.time()
  
  results_df = scrape_links(links, saved_names)
  results_df.to_excel('output.xlsx', index=False)
  end = time.time()
  
  execution_time = "{:.2f}".format(end - start) + " seconds"
  
  ic(execution_time)

if __name__ == "__main__":
    main()
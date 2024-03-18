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

start = time.time()

# def team_score():
#     away_score = (wait.until(
#     EC.presence_of_element_located((By.CLASS_NAME, 'boxDetails_awayScore__39mL_'))
#     ).text)

#     home_score = (wait.until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'boxDetails_homeScore__24V0P'))
#     ).text)

#     # div_element = driver.find_elements(By.CLASS_NAME, 'boxDetails_teamName__1OFCB')
#     div_element = wait.until(
#         EC.presence_of_all_elements_located((By.CLASS_NAME, 'boxDetails_teamName__1OFCB'))
#     )


#     away_team = div_element[0].find_element(By.TAG_NAME, "h2").text
#     home_team = div_element[1].find_element(By.TAG_NAME, "h2").text
#     print(f"{away_team} {away_score} {home_score} {home_team}")



    
# Replace this with the path to your downloaded ChromeDriver
chrome_driver_path = '/Users/samfeldman/Downloads/chromedriver-mac-arm64/chromedriver'

driver = initialize_driver(chrome_driver_path)

page_link = 'https://colleges.wearecollegetennis.com/Results/Completed?gender=MALE&conference=Ivy_League'

driver.get(page_link)

wait = WebDriverWait(driver, 10)
# wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

click_cookie_button(driver)

click_load_more(driver, 2)

links = get_button_links(driver)


test_links = [
  'https://colleges.wearecollegetennis.com/ClemsonUniversityM/Team/scorecard/C09CD3FF-7676-4675-944B-973FBAA59F40',#]
    'https://colleges.wearecollegetennis.com/AlabamaStateUniversityM/Team/scorecard/AF6C7F8D-7026-4D49-9FE1-EF1B5C0D1A37',
    'https://colleges.wearecollegetennis.com/UniversityOfNebraskaM/Team/scorecard/D998640E-06BC-46BC-A15E-B5D31992C89C'  
]

main_df = pd.DataFrame()
count = 0
for link in test_links:
    # print(link)
    df = scrape_box_score(driver, link)
    main_df = pd.concat([main_df, df], ignore_index=True)
    print(f"Scraped {count + 1} of {len(test_links)}")
    count += 1
main_df.to_excel('output.xlsx', index=False)

# url = 'https://colleges.wearecollegetennis.com/PrincetonUniversityM/Team/scorecard/F0EB1E20-0E19-4614-A2BF-BDB8591159A0'
# url = 'https://colleges.wearecollegetennis.com/YaleUniversityM/Team/scorecard/33B765EF-D1DB-49D4-83CD-5349233F7408'
# url = 'https://colleges.wearecollegetennis.com/UniversityOfCaliforniaSantaBarbaraM/Team/scorecard/6993C9ED-F069-47AF-A5A6-0257042A2813'
# df = scrape_box_score(url)
# df.to_excel('output.xlsx', index=False)


# input("Press Enter to continue...")

driver.quit()

end = time.time()
print(f"Time elapsed: {end - start:.2f} seconds")

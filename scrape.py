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

wait = WebDriverWait(driver, 10)
# wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

# try:
        
#         cookie_button = WebDriverWait(driver, 5).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, "cb-enable"))
#         )
#         cookie_button.click()
#         print("clicked cookie button")
#         # Wait a brief moment for the cookie consent to process the dismissal
#         WebDriverWait(driver, 5).until(EC.invisibility_of_element(cookie_button))
# except Exception as e:
#     print(f"Error clicking cookie button: {e}")

# times_clicked = 0

# for i in range(1):
    
#     try:
#         wait_time = 10
#         load_more_button = WebDriverWait(driver, wait_time).until(
#         EC.presence_of_element_located((By.XPATH, "//button[@data-testid='PDM-loadMore-onLoadMoreButton']")))
#         WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='PDM-loadMore-onLoadMoreButton']"))
#         )
#         ActionChains(driver).move_to_element(load_more_button).perform()
#         load_more_button.click()
#         times_clicked += 1
#         print(f"clicked load more button {times_clicked}")
        
        
#     except Exception as e:
#         # print(f"Error clicking button: {e}")
#         print("done loading")
# button_index = 0
# buttons = driver.find_elements(By.CLASS_NAME, 'link_linkCell__jIQoh')
# # print(buttons[0].get_attribute('href'))
# links = []
# for button in buttons:
#     # print(button.get_attribute('href'))
#     button_url = button.get_attribute('href')
#     links.append(button_url)
# # print(len(links))

# driver.get(links[0])
# print(driver.title)
# url = 'https://colleges.wearecollegetennis.com/ClemsonUniversityM/Team/scorecard/C09CD3FF-7676-4675-944B-973FBAA59F40'
# url = 'https://colleges.wearecollegetennis.com/AlabamaStateUniversityM/Team/scorecard/AF6C7F8D-7026-4D49-9FE1-EF1B5C0D1A37'
# url = 'https://colleges.wearecollegetennis.com/UniversityOfNebraskaM/Team/scorecard/D998640E-06BC-46BC-A15E-B5D31992C89C'
# print(driver.title)
# team_score()





test_links = [
  'https://colleges.wearecollegetennis.com/ClemsonUniversityM/Team/scorecard/C09CD3FF-7676-4675-944B-973FBAA59F40']
#     'https://colleges.wearecollegetennis.com/AlabamaStateUniversityM/Team/scorecard/AF6C7F8D-7026-4D49-9FE1-EF1B5C0D1A37',
#     'https://colleges.wearecollegetennis.com/UniversityOfNebraskaM/Team/scorecard/D998640E-06BC-46BC-A15E-B5D31992C89C'  
# ]

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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import time as time

start = time.time()

def team_score():
    away_score = (wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, 'boxDetails_awayScore__39mL_'))
    ).text)

    home_score = (wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'boxDetails_homeScore__24V0P'))
    ).text)

    # div_element = driver.find_elements(By.CLASS_NAME, 'boxDetails_teamName__1OFCB')
    div_element = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'boxDetails_teamName__1OFCB'))
    )


    away_team = div_element[0].find_element(By.TAG_NAME, "h2").text
    home_team = div_element[1].find_element(By.TAG_NAME, "h2").text
    print(f"{away_team} {away_score} {home_score} {home_team}")

def clip_school(school: str):
    return school[:len(school) - 4]
# Replace this with the path to your downloaded ChromeDriver
chrome_driver_path = '/Users/samfeldman/Downloads/chromedriver-mac-arm64/chromedriver'

# Initialize the WebDriver with the specified path
service = Service(executable_path=chrome_driver_path)

# Your scraping logic here
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# url = 'https://colleges.wearecollegetennis.com/Results/Completed?'
url = 'https://colleges.wearecollegetennis.com/Results/Completed?gender=MALE&division=DIVISION_1&conference=Ivy_League'

driver.get(url)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

try:
        
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cb-enable"))
        )
        cookie_button.click()
        print("clicked cookie button")
        # Wait a brief moment for the cookie consent to process the dismissal
        WebDriverWait(driver, 5).until(EC.invisibility_of_element(cookie_button))
except Exception as e:
    print(f"Error clicking cookie button: {e}")

times_clicked = 0

for i in range(1):
    
    try:
        wait_time = 10
        load_more_button = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.XPATH, "//button[@data-testid='PDM-loadMore-onLoadMoreButton']")))
        WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='PDM-loadMore-onLoadMoreButton']"))
        )
        ActionChains(driver).move_to_element(load_more_button).perform()
        load_more_button.click()
        times_clicked += 1
        print(f"clicked load more button {times_clicked}")
        
        
    except Exception as e:
        # print(f"Error clicking button: {e}")
        print("done loading")
button_index = 0
buttons = driver.find_elements(By.CLASS_NAME, 'link_linkCell__jIQoh')
# print(buttons[0].get_attribute('href'))
links = []
for button in buttons:
    # print(button.get_attribute('href'))
    button_url = button.get_attribute('href')
    links.append(button_url)
# print(len(links))

# driver.get(links[0])
# print(driver.title)
# url = 'https://colleges.wearecollegetennis.com/ClemsonUniversityM/Team/scorecard/C09CD3FF-7676-4675-944B-973FBAA59F40'
# url = 'https://colleges.wearecollegetennis.com/AlabamaStateUniversityM/Team/scorecard/AF6C7F8D-7026-4D49-9FE1-EF1B5C0D1A37'
# url = 'https://colleges.wearecollegetennis.com/UniversityOfNebraskaM/Team/scorecard/D998640E-06BC-46BC-A15E-B5D31992C89C'
# print(driver.title)
# team_score()

def scrape_box_score(url: str):
    
    driver.get(url)

    excel_data = []


    wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'boxDetails_boxDetails__2vQeJ'))
    )

    date_div = driver.find_element(By.CLASS_NAME, 'boxDetails_boxDetails__2vQeJ')

    date_string = date_div.find_element(By.TAG_NAME, "time").text
    date_part = date_string.split(" / ")[0]

    # Parse the date
    date_format = "%b %d (%a), %Y"
    parsed_date = datetime.strptime(date_part, date_format)

    # Format the date into mm/dd/yyyy
    formatted_date = parsed_date.strftime("%m/%d/%Y")

    print(formatted_date)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'boxDetails_teamName__1OFCB')))

    # away boxDetails_teamName__1OFCB 
    # home boxDetails_team__1OjSB


    teams = driver.find_elements(By.CLASS_NAME, 'boxDetails_teamName__1OFCB')

    away_team_name = teams[0].find_element(By.TAG_NAME, "h2").text
    home_team_name = teams[1].find_element(By.TAG_NAME, "h2").text

    # away boxDetails_awayScore__39mL_
    away_team_score = int(driver.find_element(By.CLASS_NAME, 'boxDetails_awayScore__39mL_').text)
    # home boxDetails_homeScore__24V0P
    home_team_score = int(driver.find_element(By.CLASS_NAME, 'boxDetails_homeScore__24V0P').text)

    if away_team_score > home_team_score:
        winning_team = away_team_name
        winning_score = away_team_score
        losing_team = home_team_name
        losing_score = home_team_score
    else:
        winning_team = home_team_name
        winning_score = home_team_score
        losing_team = away_team_name
        losing_score = away_team_score

    dual_score = f"{winning_score}-{losing_score}"

    print(f"{clip_school(away_team_name)} AWAY vs {clip_school(home_team_name)} HOME")

    print(f"{clip_school(winning_team)} def {clip_school(losing_team)} {winning_score} - {losing_score}")

    if away_team_name[len(away_team_name) - 3:] == "(M)":
        gender = "Male"
    if away_team_name[len(away_team_name) - 3:] == "(W)":
        gender = "Female" 
    print(f"Gender: {gender}")    
    print()
    wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'tieMatchUp_tieMatchUp__1_Bfm'))
    )

    match_divs = driver.find_elements(By.CLASS_NAME, 'tieMatchUp_tieMatchUp__1_Bfm')

    cached_names = {}

    for match in match_divs:
        info = match.find_element(By.TAG_NAME, "h3").text
        line = info.split(" ")[0]
        type = info.split(" ")[1]
        print(f"{line} {type}")
        
        winner_name = ""
        winner_partner_name = ""
        winner_college = ""
        loser_name = ""
        loser_partner_name = "" 
        loser_college = "" 
        
        players = match.find_elements(By.CLASS_NAME, 'tieMatchUp_side__3iIKA')
        winning_player_score = []
        losing_player_score = []
        
        valid_match = []
        
        for idx in range(2):
        
            player = players[idx]

        # tieMatchUp_flag__4biXR UF
        # tieMatchUp_winnerIcon__CTmd5 WIN
        # tieMatchUp_flag__4biXR RET
            
            result = "Lost"
            
                
            player_divs = player.find_elements(By.TAG_NAME, 'div')
                
            for player_div in player_divs:
                classes = player_div.get_attribute("class").split()

                if "tieMatchUp_flag__4biXR" in classes:
                    flag_type = player_div.find_element(By.TAG_NAME, "abbr").text
                    if flag_type == "W/O":
                        result = "Walkover"
                    if flag_type == "DEF":
                        result = "Default"
                if "tieMatchUp_winnerIcon__CTmd5" in classes:
                    result = "Won"
                # if "tieMatchUp_flag__4biXR" in classes:
                #     result = ""
            
            valid_match.append(result)
            # result = "Lost"
            
            # if "tieMatchUp_winner__2EtgR" in player.get_attribute("class").split():
            #     result = "Won"
            
            original_window = driver.current_window_handle 
            
            name = player.find_element(By.CLASS_NAME, 'tieMatchUp_name__1lTsZ')
        
            full_names = [] 
        
            name_links = name.find_elements(By.TAG_NAME, "a")
            
            

            for link in name_links:
                name_link = link.get_attribute("href")
                short_name = link.text
                if short_name in cached_names:
                    full_names.append(cached_names[link.text])
                else:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(name_link)
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'teamBanner_playerName__2PcjI'))) 
                    full_name = driver.find_element(By.CLASS_NAME, 'teamBanner_playerName__2PcjI').text
                    full_names.append(full_name)
                    cached_names[short_name] = full_name
                    driver.close()
                    driver.switch_to.window(original_window)
        
                
            # driver.back()
            # driver.get(url)
            
                
            if result == "Won":
                if type == "Doubles":
                    # pair_names = name.text.split(" /")
                    winner_name = full_names[0]
                    winner_partner_name = full_names[1]
                else:   
                    winner_name = full_names[0] 
                    
                if idx == 0:
                    winner_college = clip_school(away_team_name)
                else:
                    winner_college = clip_school(home_team_name)
                    
            if result == "Lost":
                if type == "Doubles":
                    # pair_names = name.text.split(" /")
                    loser_name = full_names[0]
                    loser_partner_name = full_names[1]
                else:   
                    loser_name = full_names[0]

                if idx == 0:
                    loser_college = clip_school(away_team_name)
                else:
                    loser_college = clip_school(home_team_name)
            
            
            # 
            # tieMatchUp_winnerIcon__CTmd5
            wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'tieMatchUp_score__2WkUA'))
            )
            score = player.find_elements(By.CLASS_NAME, 'tieMatchUp_score__2WkUA')
            games_score = ''
            for s in score:
                set_score = ""
                
                #if tie_break
                
                if len(s.text) >= 3: 
                    #if not super_tiebreak
                    if s.text[0] == "1":
                        set_score = s.text[2] + s.text[3]
                    elif s.text[0] != "[": 
                        for i in s.text:
                            if i == " ":
                                set_score += "("
                            else:
                                set_score += i
                        set_score += ")"
                    elif s.text[0] == "[":
                        set_score = s.text[1] + s.text[2]

                else:
                    set_score = s.text
                if len(set_score) > 0 and set_score[-1] == "]":
                    set_score = set_score[:len(set_score) - 1]
                    
                    
                    
                if result == "Won":
                    winning_player_score.append(set_score)    
                if result == "Lost":
                    losing_player_score.append(set_score) 
                
                
                games_score += set_score + " "
            # print(name.text, games_score, result)
            
        match_score = ""
        
        if len(winning_player_score) != 0:
            for i in range(len(winning_player_score)):
                
                if winning_player_score[i][0] == "7" and len(winning_player_score[i]) != 1:
                    match_score += winning_player_score[i][0] + "-" + losing_player_score[i] + ", "
                elif losing_player_score[i][0] == "7" and len(losing_player_score[i]) != 1:
                    match_score += winning_player_score[i][0] + "-" + losing_player_score[i][0] + winning_player_score[i][1:] + ", " 
                else:
                    match_score += winning_player_score[i] + "-" + losing_player_score[i] + ", "
                
            match_score = match_score[:len(match_score) - 2] 

        if valid_match == ["Lost", "Lost"]:
            loser_college = ""
            loser_name = ""
            loser_partner_name = ""

        row_data = {
                "Date(mm/dd/yyyy)": formatted_date,
                "Gender": gender,
                "Position": f"{line} {type}",
                "Winner Name": winner_name,
                "Winner Partner Name": winner_partner_name,
                "Winner College": winner_college,
                "Loser Name": loser_name,
                "Loser Partner Name": loser_partner_name,
                "Loser College": loser_college,
                "Score": match_score,
                "Winner Team": "",
                "Loser Team": "",
                "Team Score": ""
                
            }
        excel_data.append(row_data)
        print()



    # while button_index < len(buttons):
    #     try:
    #         # Wait for the button to be clickable and then click it
    #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(buttons[button_index])).click()
            
    #         # Wait for the new page to load and perform the desired actions
    #         # For example, print the current URL
    #         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'boxDetails_teamName__1OFCB')))
    #         team_score() 
    #         # Go back to the original page
    #         driver.back()
            
    #         # Wait for the original page to load
    #         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'link_linkCell__jIQoh')))
            
    #         # Re-find all the buttons since the DOM has been refreshed
    #         buttons = driver.find_elements(By.CLASS_NAME, 'link_linkCell__jIQoh')
            
    #         # Increment the index to move to the next button
    #         button_index += 1
            
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         break  # If there's an error, exit the loop




    df = pd.DataFrame(excel_data)
    df.at[0, "Winner Team"] = clip_school(winning_team)
    df.at[0, "Loser Team"] = clip_school(losing_team)
    df.at[0, "Team Score"] = dual_score
    blank_rows = pd.DataFrame([[""] * len(df.columns)] * 2)
    df = pd.concat([df.iloc[:0], blank_rows, df.iloc[0:]], ignore_index=False)
    
    return df

test_links = [
  'https://colleges.wearecollegetennis.com/ClemsonUniversityM/Team/scorecard/C09CD3FF-7676-4675-944B-973FBAA59F40',
    'https://colleges.wearecollegetennis.com/AlabamaStateUniversityM/Team/scorecard/AF6C7F8D-7026-4D49-9FE1-EF1B5C0D1A37',
    'https://colleges.wearecollegetennis.com/UniversityOfNebraskaM/Team/scorecard/D998640E-06BC-46BC-A15E-B5D31992C89C'  
]

main_df = pd.DataFrame()
count = 0
for link in links:
    # print(link)
    df = scrape_box_score(link)
    main_df = pd.concat([main_df, df], ignore_index=True)
    print(f"Scraped {count + 1} of {len(links)}")
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
print(f"Time elapsed: {end - start} seconds")
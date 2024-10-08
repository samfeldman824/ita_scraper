import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
from urllib.parse import urlparse, parse_qs
import time as time
import configparser
from icecream import ic
import contextlib
import random


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def initialize_driver():
    # Initialize the Chrome driver
    config = read_config()
    chrome_driver_path = config['Setup']['chrome_driver_path']

    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    ] 
     
    service = Service(executable_path=chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

def clip_school(school: str) -> str:
    """
    Removes the last 4 characters from the given school name.

    Args:
        school (str): The name of the school.

    Returns:
        str: The school name with the last 4 characters removed.
    """
    return school[:len(school) - 4]

def get_date(driver: webdriver.Chrome) -> str:
    """
    Retrieves the date from ita box score page.

    Args:
        driver: The WebDriver instance used to interact with the web page.

    Returns:
        A formatted date string in the format mm/dd/yyyy.
    """
    WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'boxDetails_boxDetails__2dpw_'))
    )

    date_div = driver.find_element(By.CLASS_NAME, 'boxDetails_boxDetails__2dpw_')

    date_string = date_div.find_element(By.TAG_NAME, "time").text
    date_part = date_string.split(" / ")[0]

    # Parse the date
    date_format = "%b %d (%a), %Y"
    parsed_date = datetime.strptime(date_part, date_format)

    # Format the date into mm/dd/yyyy
    formatted_date = parsed_date.strftime("%m/%d/%Y")

    return formatted_date

def get_teams_and_score(driver: webdriver.Chrome) -> tuple[str, str, str, str, int, int, str, str]:
    """
    Retrieves the teams, scores, and gender information from ita box score page.

    Args:
        driver: The WebDriver instance used to interact with the web page.

    Returns:
        A tuple containing the following information:
        - away_team_name: The name of the away team.
        - home_team_name: The name of the home team.
        - winning_team: The name of the winning team.
        - losing_team: The name of the losing team.
        - winning_score: The score of the winning team.
        - losing_score: The score of the losing team.
        - dual_score: The combined score in the format "winning_score-losing_score".
        - gender: The gender of the teams (either "Male" or "Female").

    """
    wait = WebDriverWait(driver, 10)
    
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'boxDetails_team__2bSob')))

    # away boxDetails_teamName__1OFCB 
    # home boxDetails_team__1OjSB

    teams = driver.find_elements(By.CLASS_NAME, 'boxDetails_team__2bSob')

    away_team_name = teams[0].find_element(By.TAG_NAME, "h2").text
    home_team_name = teams[1].find_element(By.TAG_NAME, "h2").text

    # away boxDetails_awayScore__39mL_
    away_team_score = int(driver.find_element(By.CLASS_NAME, 'boxDetails_awayScore__2GSN-').text)
    # home boxDetails_homeScore__24V0P
    home_team_score = int(driver.find_element(By.CLASS_NAME, 'boxDetails_homeScore__2tbNy').text)

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
    ic(gender)
    print()
    
    return away_team_name, home_team_name, winning_team, losing_team, winning_score, losing_score, dual_score, gender

def click_cookie_button(driver: webdriver.Chrome) -> None:
    """
    Clicks the cookie button on ita results page.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.

    Raises:
        Exception: If there is an error clicking the cookie button.

    Returns:
        None
    """
    # osano-cm-manage button class for manage preferences
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cb-enable"))
        )
        cookie_button.click()
        print("clicked cookie button")
        WebDriverWait(driver, 5).until(EC.invisibility_of_element(cookie_button))
    except Exception as e:
        print(f"Error clicking cookie button: {e}")

def click_load_more(driver: webdriver.Chrome, num_clicks: int) -> None:
    """
    Clicks the 'Load More' button on a webpage a specified number of times.
    
    Args:
        driver (webdriver.Chrome): The Chrome webdriver instance.
        num_clicks (int): The number of times to click the 'Load More' button.
    
    Returns:
        None 
    """
    for i in range(num_clicks):
        try:
            wait_time = 10
            load_more_button = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-testid='PDM-loadMore-onLoadMoreButton']")))
            WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='PDM-loadMore-onLoadMoreButton']")))
            
            ActionChains(driver).move_to_element(load_more_button).perform()
            load_more_button.click()
            print(f"Clicked load more button {i + 1} times") 
            
        except Exception as e:
            print("done loading")

def get_button_links(driver: webdriver.Chrome) -> list[str]:
    """
    Retrieves the URLs of buttons to box scores on the webpage.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.

    Returns:
        list[str]: A list of URLs corresponding to the buttons found on the webpage.
    """
    links = []
    
    wait = WebDriverWait(driver, 10)
    buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'link_linkCell__jIQoh')))

    # buttons = driver.find_elements(By.CLASS_NAME, 'link_linkCell__jIQoh')
    
    for button in buttons:
        button_url = button.get_attribute('href')
        links.append(button_url)
    
    return links
    
def scrape_box_score(driver: webdriver.Chrome, url: str, saved_names: dict[str, str]) -> pd.DataFrame:
    """
    Scrapes the box score data from a given URL of box score.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        url (str): The URL of the box score page.
        saved_names (dict[str, str]): A dictionary containing cached player names.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped box score data.
    """
    wait = WebDriverWait(driver, 2)
    
    driver.get(url)

    excel_data = []
    
    formatted_date = get_date(driver)
    
    ic(formatted_date)

    away_team_name, home_team_name, winning_team, losing_team, winning_score,\
        losing_score, dual_score, gender = get_teams_and_score(driver)

    WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'tieMatchUp_tieMatchUp__2tiv0'))
    )

    match_divs = driver.find_elements(By.CLASS_NAME, 'tieMatchUp_tieMatchUp__2tiv0')

    cached_names = saved_names 
    
    for match in match_divs:
        info = match.find_element(By.TAG_NAME, "h3").text
        line = info.split(" ")[0]
        type = info.split(" ")[1]
        # print(f"{line} {type}")
        
        winner_name = ""
        winner_partner_name = ""
        winner_college = ""
        loser_name = ""
        loser_partner_name = "" 
        loser_college = "" 
        
        players = match.find_elements(By.CLASS_NAME, 'tieMatchUp_side__EmIHe')
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

                if "tieMatchUp_flag__2Z23m" in classes:
                    flag_type = player_div.find_element(By.TAG_NAME, "abbr").text
                    if flag_type == "W/O":
                        result = "Walkover"
                    if flag_type == "DEF":
                        result = "Default"
                if "tieMatchUp_winnerIcon__Y3wof" in classes:
                    result = "Won"
                # if "tieMatchUp_flag__4biXR" in classes:
                #     result = ""
            
            valid_match.append(result)
            # result = "Lost"
            
            # if "tieMatchUp_winner__2EtgR" in player.get_attribute("class").split():
            #     result = "Won"
            
            original_window = driver.current_window_handle 
            
            name = player.find_element(By.CLASS_NAME, 'tieMatchUp_name__38vwK')
        
            full_names = [] 
        
            name_links = name.find_elements(By.TAG_NAME, "a")
            
            
            for link in name_links:
                short_name = link.text
                name_link = link.get_attribute("href")
                parsed_url = urlparse(name_link)
                player_id = parse_qs(parsed_url.query).get('s', [None])[0][8:]
                # short_name = link.text
                if player_id in cached_names:
                    full_names.append(cached_names[player_id])
                else:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    
                    try:
                        driver.get(name_link)
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'teamBanner_playerName__3t6Mj'))) 
                        full_name = driver.find_element(By.CLASS_NAME, 'teamBanner_playerName__3t6Mj').text
                        full_name = ' '.join(full_name.replace('\n', ' ').split())
                        full_names.append(full_name)
                        cached_names[player_id] = full_name
                    except:
                        full_names.append(short_name)
                        cached_names[player_id] = short_name
                    
                    driver.close()
                    driver.switch_to.window(original_window)
                        
                    
                
            # driver.back()
            # driver.get(url)
            
                
            if result == "Won" and len(full_names) != 0:
                if type == "Doubles":
                    try:
                        winner_name = full_names[0]
                        winner_partner_name = full_names[1]
                    except:
                        continue
                    
                else:   
                    winner_name = full_names[0] 
                    
                if idx == 0:
                    winner_college = clip_school(away_team_name)
                else:
                    winner_college = clip_school(home_team_name)
                    
            if result == "Lost" and len(full_names) != 0:
                if type == "Doubles":
                    try:
                        loser_name = full_names[0]
                        loser_partner_name = full_names[1]
                    except:
                        continue
                else:   
                    loser_name = full_names[0]

                if idx == 0:
                    loser_college = clip_school(away_team_name)
                else:
                    loser_college = clip_school(home_team_name)
            
            
            # 
            # tieMatchUp_winnerIcon__CTmd5
            wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'tieMatchUp_score__22eNa'))
            )
            score = player.find_elements(By.CLASS_NAME, 'tieMatchUp_score__22eNa')
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

        if type == "Doubles" and winner_name != "":
            print(f" {line} {type}")
            print(f"{winner_name} & {winner_partner_name} def {loser_name} & {loser_partner_name} {match_score}")
        if type == "Singles" and winner_name != "":
            print(f" {line} {type}")
            print(f"{winner_name} def {loser_name} {match_score}")
        
        
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

    saved_names.update(cached_names)
    # with open('saved_names.json', 'w') as f:
    #     json.dump(saved_names, f)

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

division_dict = {
    '1': 'DIVISION_1',
    '2': 'DIVISION_2',
    '3': 'DIVISION_3',
    'naia': 'NAIA',
    'juco': 'NJCAA',
}    

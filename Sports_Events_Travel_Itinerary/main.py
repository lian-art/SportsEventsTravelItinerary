#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import lxml
import lxml.etree
import re
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import time
import json
from urllib.request import urlopen
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import matplotlib.pyplot as plt


# ------------------------------------------------Sports Data Crawler ----------------------------------------------

def MLB_scrapper_func():
    # MLB Scraper function
    # scrape the MLB data from the stubhub
    import time
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://www.stubhub.com/mlb-tickets")
    driver.implicitly_wait(20)
    time.sleep(10)
    while True:
        # if there is any see more bottun, click it
        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'See More')]").click()
            time.sleep(0.5)
        # else break the loop
        except:
            break
            # scroll down to the end
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_text = driver.page_source
    driver.quit()
    # print(page_text)
    # use BeautifulSoup to read and clean the data
    soup = BeautifulSoup(page_text, 'html.parser')
    span = soup.find_all("span")
    for s in span:
        if "locations" in s.text:
            target = s
    a_s = target.parent.parent.find_all("a")
    # define the elements we want
    date = []
    day = []
    time = []
    home_team = []
    away_team = []
    location = []
    city = []
    states = []
    country = []
    price = []
    cnt = 0
    # clean and get all the information needed
    for a in a_s:
        # remove the season package ticket
        if "TBD at" not in str(a.get_text("[SEP]")):
            tickets = a.time.parent.parent.parent.get_text("[SEP]")
            ticket = tickets.split("[SEP]")
            # find the year
            datetime_object = datetime.strptime(ticket[0][0:3], "%b")
            month_number = datetime_object.month
            currentMonth = datetime.now().month
            # get the date
            if month_number < currentMonth:
                date.append(ticket[0] + ' 23')
            else:
                date.append(ticket[0] + ' 22')
            # day
            day.append(ticket[1])
            # time
            time.append(ticket[2])
            # team names
            t = ticket[3].split(':')
            t = t[0].split('at ')
            if len(t) > 1:
                home_team.append(t[1].strip())
                away_team.append(t[0].strip())
            else:
                home_team.append(pd.NA)
                away_team.append(pd.NA)
                # location
            loc = ticket[4].split(", ")
            if len(loc) == 4:
                if "TBD" in loc[0]:
                    sta = loc[0].split("TBD -\xa0")
                    location.append(sta[1])
                    city.append(loc[1])
                    states.append(loc[2])
                    country.append(loc[3])
                else:
                    location.append(loc[0])
                    city.append(loc[1])
                    states.append(loc[2])
                    country.append(loc[3])
            elif len(loc) == 3:
                if "TBD" in loc[0]:
                    sta = loc[0].split("TBD -\xa0")
                    location.append(sta[1])
                    city.append(loc[1])
                    states.append('')
                    country.append(loc[2])
                else:
                    location.append(loc[0])
                    city.append(loc[1])
                    states.append('')
                    country.append(loc[2])
                    # price
            if ticket[-1].startswith('$'):
                price.append(ticket[-1])
            elif ticket[-4].startswith('$'):
                price.append(ticket[-4])
            else:
                price.append(pd.NA)
    # get the final dataframe
    data = list(zip(home_team, away_team, location, city, states, country, date, day, time, price))
    data = pd.DataFrame(data,
                        columns=['Home_Team', 'Away_Team', 'Arena', 'City', 'State', 'Country', 'Date', 'Day', 'Time',
                                 'Price'])
    data["Home_Team"] = data["Home_Team"].replace(r'^\s*$', np.nan, regex=True)
    data["Away_Team"] = data["Away_Team"].replace(r'^\s*$', np.nan, regex=True)
    for i in range(len(data)):
        if data["Date"][i] != "TBD":
            data["Date"][i] = datetime.strptime(data["Date"][i], "%b %d %y")
            data["Date"][i] = datetime.strftime(data["Date"][i], "%Y-%m-%d")
            data["Date"][i] = datetime.strptime(data["Date"][i], "%Y-%m-%d").date()
        if data["Home_Team"][i] == np.nan or data["Away_Team"][i] == np.nan:
            data = data.drop(index=i)
    MLB_data = data.reset_index(drop=True)
    print("                    ***MLB Data***")
    print("------------------------------------------------------------")
    print(MLB_data.head())
    MLB_data.to_csv('./MLB_data.csv')
    return MLB_data


# ------------------------------------------------Sports Data Crawler ----------------------------------------------

def NFL_scrapper_func():
    # NFL Scraper function
    # scrape the NFL data from the stubhub
    import time
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(
        "https://www.stubhub.com/nfl-tickets/?gcid=C12289X486&utm_source=google&utm_medium=paid-search&utm_sub_medium=prospecting&utm_term=tm&utm_campaign=33820630%3Adefault&utm_content=default&keyword=1160920960_kwd-113741604_c&creative=249920920219&utm_kxconfid=s2rshsbmv&kwt=tm&mt=e&kw=stubhub&MetroRegionID=&psc=&ps=&ps_p=0&ps_c=33820630&ps_ag=1160920960&ps_tg=kwd-113741604&ps_ad=249920920219&ps_adp=&ps_fi=&ps_li=&ps_lp=9005925&ps_n=g&ps_d=c&PCID=PSUSGOOSHGBR56BB04400F&gclid=Cj0KCQjwmouZBhDSARIsALYcouooEqqgILz8he7beWGMZaL1vodi8XfPGqZASsqYGC3Tv0WHfKVHqAYaAiQOEALw_wcB&gridFilterType=0")
    driver.implicitly_wait(30)
    time.sleep(10)
    while True:
        # if there is any see more bottun, click it
        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'See More')]").click()
        # else break the loop
        except:
            break
            # scroll down to the end
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_text = driver.page_source

    driver.quit()
    # print(page_text)
    # use BeautifulSoup to read and clean the data
    soup = BeautifulSoup(page_text, 'html.parser')
    span = soup.find_all("span")
    for s in span:
        if "locations" in s.text:
            target = s
    a_s = target.parent.parent.find_all("a")
    # define the elements we want
    date = []
    day = []
    time = []
    home_team = []
    away_team = []
    location = []
    city = []
    states = []
    country = []
    price = []
    cnt = 0
    # clean and get all the information needed
    for a in a_s:
        # remove the season package ticket
        if "TBD" not in str(a.get_text("[SEP]")) and "Tailgate Party " not in str(a.get_text("[SEP]")):
            try:
                tickets = a.time.parent.parent.parent.get_text("[SEP]")
                ticket = tickets.split("[SEP]")
                # find the year
                datetime_object = datetime.strptime(ticket[0][0:3], "%b")
                month_number = datetime_object.month
                currentMonth = datetime.now().month
                # get the date
                if month_number < currentMonth:
                    date.append(ticket[0] + ' 23')
                else:
                    date.append(ticket[0] + ' 22')
                # day
                day.append(ticket[1])
                # time
                time.append(ticket[2])
                # team names
                t = ticket[3].split(':')
                t = t[0].split('at ')
                if len(t) > 1:
                    home_team.append(t[1].strip())
                    away_team.append(t[0].strip())
                else:
                    home_team.append(pd.NA)
                    away_team.append(pd.NA)
                    # location
                loc = ticket[4].split(", ")
                if len(loc) == 4:
                    if "TBD" in loc[0]:
                        sta = loc[0].split("TBD -\xa0")
                        location.append(sta[1])
                        city.append(loc[1])
                        states.append(loc[2])
                        country.append(loc[3])
                    else:
                        location.append(loc[0])
                        city.append(loc[1])
                        states.append(loc[2])
                        country.append(loc[3])
                elif len(loc) == 3:
                    if "TBD" in loc[0]:
                        sta = loc[0].split("TBD -\xa0")
                        location.append(sta[1])
                        city.append(loc[1])
                        states.append('')
                        country.append(loc[2])
                    else:
                        location.append(loc[0])
                        city.append(loc[1])
                        states.append('')
                        country.append(loc[2])
                        # price
                if ticket[-1].startswith('$'):
                    price.append(ticket[-1])
                elif ticket[-4].startswith('$'):
                    price.append(ticket[-4])
                else:
                    price.append(pd.NA)
            except:
                continue
    # get the final dataframe
    data = list(zip(home_team, away_team, location, city, states, country, date, day, time, price))
    data = pd.DataFrame(data,
                        columns=['Home_Team', 'Away_Team', 'Arena', 'City', 'State', 'Country', 'Date', 'Day', 'Time',
                                 'Price'])
    data["Home_Team"] = data["Home_Team"].replace(r'^\s*$', np.nan, regex=True)
    data["Away_Team"] = data["Away_Team"].replace(r'^\s*$', np.nan, regex=True)
    for i in range(len(data)):
        if data["Date"][i] != "TBD":
            data["Date"][i] = datetime.strptime(data["Date"][i], "%b %d %y")
            data["Date"][i] = datetime.strftime(data["Date"][i], "%Y-%m-%d")
            data["Date"][i] = datetime.strptime(data["Date"][i], "%Y-%m-%d").date()
        if data["Home_Team"].isna()[i] or data["Away_Team"].isna()[i]:
            data = data.drop(index=i)
    NFL_data = data.reset_index(drop=True)
    print("                    ***NFL Data***")
    print("------------------------------------------------------------")
    print(NFL_data.head())
    NFL_data.to_csv('./NFL_data.csv')
    return NFL_data


# ------------------------------------------------Sports Data Crawler ----------------------------------------------

def NBA_scrapper_func():
    # NBA Scraper function
    # scrape the NBA data from the stubhub
    import time
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.stubhub.com/nba-tickets/grouping/115/")
    driver.implicitly_wait(30)
    time.sleep(10)
    while True:
        # if there is any see more bottun, click it
        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'See More')]").click()
            time.sleep(1)
        # else break the loop
        except:
            break
            # scroll down to the end
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_text = driver.page_source
    driver.quit()
    # print(page_text)
    # use BeautifulSoup to read and clean the data
    soup = BeautifulSoup(page_text, 'html.parser')
    span = soup.find_all("span")
    for s in span:
        if "location" in s.text:
            target = s
    a_s = target.parent.parent.find_all("a")
    # define the elements we want
    date = []
    day = []
    time = []
    home_team = []
    away_team = []
    location = []
    city = []
    states = []
    country = []
    price = []
    cnt = 0
    # clean and get all the information needed
    for a in a_s:
        # remove the season package ticket
        if "Season Package" not in str(a.get_text("[SEP]")):
            tickets = a.time.parent.parent.parent.get_text("[SEP]")
            ticket = tickets.split("[SEP]")
            # find the year
            datetime_object = datetime.strptime(ticket[0][0:3], "%b")
            month_number = datetime_object.month
            currentMonth = datetime.now().month
            # get the date
            if month_number < currentMonth:
                date.append(ticket[0] + ' 23')
            else:
                date.append(ticket[0] + ' 22')
            # day
            day.append(ticket[1])
            # time
            time.append(ticket[2])
            # team names

            if "Preseason" not in ticket[3]:
                t = ticket[3].split('at ')
                if len(t) > 1:
                    home_team.append(t[1].strip())
                    away_team.append(t[0].strip())
            else:
                t = ticket[3].split('at ')
                if len(t) > 1:
                    if "Preseason" in t[1]:
                        home_team.append(t[1].strip())
                        away_team.append(t[0].strip() + " Preseason")
                    else:
                        home_team.append(t[1].strip() + " Preseason")
                        away_team.append(t[0].strip())

                        # location
            loc = ticket[4].split(", ")
            if len(loc) == 4:
                if "TBD" in loc[0]:
                    sta = loc[0].split("TBD -\xa0")
                    location.append(sta[1])
                    city.append(loc[1])
                    states.append(loc[2])
                    country.append(loc[3])
                else:
                    location.append(loc[0])
                    city.append(loc[1])
                    states.append(loc[2])
                    country.append(loc[3])
            elif len(loc) == 3:
                if "TBD" in loc[0]:
                    sta = loc[0].split("TBD -\xa0")
                    location.append(sta[1])
                    city.append(loc[1])
                    states.append('')
                    country.append(loc[2])
                else:
                    location.append(loc[0])
                    city.append(loc[1])
                    states.append('')
                    country.append(loc[2])
                    # price
            if ticket[-1].startswith('$'):
                price.append(ticket[-1])
            else:
                price.append(' ')
    # get the final dataframe
    data = list(zip(home_team, away_team, location, city, states, country, date, day, time, price))
    data = pd.DataFrame(data,
                        columns=['Home_Team', 'Away_Team', 'Arena', 'City', 'State', 'Country', 'Date', 'Day', 'Time',
                                 'Price'])
    # change the date type
    data["Home_Team"] = data["Home_Team"].replace(r'^\s*$', np.nan, regex=True)
    data["Away_Team"] = data["Away_Team"].replace(r'^\s*$', np.nan, regex=True)
    for i in range(len(data)):
        if data["Date"][i] != "TBD":
            data["Date"][i] = datetime.strptime(data["Date"][i], "%b %d %y")
            data["Date"][i] = datetime.strftime(data["Date"][i], "%Y-%m-%d")
            data["Date"][i] = datetime.strptime(data["Date"][i], "%Y-%m-%d").date()
        if data["Home_Team"].isna()[i] or data["Away_Team"].isna()[i]:
            data = data.drop(index=i)
    NBA_data = data.reset_index(drop=True)
    print("                    ***NBA Data***")
    print("------------------------------------------------------------")
    print(NBA_data.head())
    # export to csv file
    NBA_data.to_csv('./NBA_data.csv')
    return NBA_data


# ------------------------------------------------Sports Data Input ----------------------------------------------

def sports():
    # call the scraper functions

    # live scraper

    # Due to the UI design of Stubhub
    # Somtimes, the prices cannot display on the front page
    # For convience, if there are no prices
    # choose to use prvious scraped data
    # mlb_data = MLB_scrapper_func()
    # try:
    #     price = int(mlb_data['Price'][0])
    # except:
    #     mlb_data = pd.read_csv("MLB_data_original.csv")
    # nfl_data = NFL_scrapper_func()
    # try:
    #     price = int(nfl_data['Price'][0])
    # except:
    #     nfl_data = pd.read_csv("NFL_data_original.csv")
    # nba_data = NBA_scrapper_func()
    # try:
    #     price = int(nba_data['Price'][0])
    # except:
    #     nba_data = pd.read_csv("NBA_data_original.csv")

    # used privious data directly

    # if you want to use the previous data, you can use this section and you need to comment out the scraper function above
    mlb_data = pd.read_csv("MLB_data_original.csv")

    nfl_data = pd.read_csv("NFL_data_original.csv")

    nba_data = pd.read_csv("NBA_data_original.csv")

    print("                   ***Sports Tickets***")
    print("--------------------------------------------------------------------------\n")
    while True:
        sport = input("Please choose the sports name from NBA, NFL, MLB\n")
        if sport.upper() == 'NBA':
            print("Your choice is: " + sport)
            data_new = nba_data
            button = 1
            break;
        elif sport.upper() == 'NFL':
            print("Your choice is: " + sport)
            data_new = nfl_data
            button = 2
            break;
        elif sport.upper() == 'MLB':
            print("Your choice is: " + sport)
            data_new = mlb_data
            button = 3
            break;
        else:
            continue
    data = data_new
    print(data.to_string())
    print("\n\n--------------------------------------------------------------------------")
    print("                   ***Event Overview***\n")
    # Event Overview
    # Based on the sports selection, show the number of tickets for repsective teams
    # NBA team information generation
    if button == 1:
        print("Your are interested in: Basketball\n")
        print("This is the overview about the number distribution of every team:")

        def die(s):
            print('[DIE] %s' % s)
            exit()

        # Two plots: one for home_team, one for away_team
        home_dict = {}
        away_dict = {}

        for i in csv.reader(open('NBA_data.csv')):
            h = i[1]
            a = i[2]
            if h == 'Home_Team':  # header
                continue

            # Split the String to get the home_team and away_team name, get rid of invalid data
            h = h.split('vs.')
            if len(h) not in [1, 2]:
                die('Invalid Home_Team Data')

            if len(h) == 2:
                if len(a) != 0:
                    die('Invalid Away_Team Data')
                a = h[1]
                h = h[0].split(':')
                if len(h) != 2:
                    die('Invalid Home_Team Data')
                h = h[1]
            else:
                h = h[0]

            h = h.split('(')[0]
            a = a.split('(')[0]
            h = h.split('-')[-1]
            a = a.split('-')[-1]

            # Create dictionary for home_team/away_team and count the ticket amount
            if h not in home_dict:
                home_dict[h] = 0
            if a not in away_dict:
                away_dict[a] = 0
            home_dict[h] += 1
            away_dict[a] += 1

        # Draw the plots
        def myplot2(fn, x, y, t, c):
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            ax.barh(x, y, color=c)
            ax.set_xlabel('Number of Tickets', fontsize=8)
            ax.set_title(t, fontsize=15)
            ax.set_ylabel('Team Name', fontsize=8)
            ax.yaxis.set_label_position('right')
            ax.tick_params(labelsize=6, left=False, bottom=False)
            ax.tick_params(axis='x', labelsize=8)
            ax.tick_params(axis='y', pad=0)

        x = list(home_dict.keys())
        y = [home_dict[i] for i in x]
        myplot2('hometeam_for_NBA.png', x, y, 'Home', 'red')

        x = list(away_dict.keys())
        y = [away_dict[i] for i in x]
        myplot2('awayteam_for_NBA.png', x, y, 'Away', 'blue')
        plt.show()

    # Similarly, draw for NFL
    elif button == 2:
        print("Your are interested in: Football\n")
        print("This is the overview about the number distribution of every team:")

        def die(s):
            print('[DIE] %s' % s)
            exit()

        home_dict = {}
        away_dict = {}

        for i in csv.reader(open('NFL_data.csv')):
            h = i[1]
            a = i[2]
            if h == 'Home_Team':  # header
                continue
            h = h.split('vs.')
            if len(h) not in [1, 2]:
                die('Invalid Home_Team Data')

            if len(h) == 2:
                if len(a) != 0:
                    die('Invalid Away_Team Data')
                a = h[1]
                h = h[0].split(':')
                if len(h) != 2:
                    die('Invalid Home_Team Data')
                h = h[1]
            else:
                h = h[0]

            h = h.split('(')[0]
            a = a.split('(')[0]
            h = h.split('-')[-1]
            a = a.split('-')[-1]

            if h not in home_dict:
                home_dict[h] = 0
            if a not in away_dict:
                away_dict[a] = 0
            home_dict[h] += 1
            away_dict[a] += 1

        def myplot2(fn, x, y, t, c):
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            ax.barh(x, y, color=c)
            ax.set_xlabel('Number of Tickets', fontsize=8)
            ax.set_title(t, fontsize=15)
            ax.set_ylabel('Team Name', fontsize=8)
            ax.yaxis.set_label_position('right')
            ax.tick_params(labelsize=6, left=False, bottom=False)
            ax.tick_params(axis='x', labelsize=8)
            ax.tick_params(axis='y', pad=0)

        x = list(home_dict.keys())
        y = [home_dict[i] for i in x]
        myplot2('hometeam_for_NFL.png', x, y, 'Home', 'red')

        x = list(away_dict.keys())
        y = [away_dict[i] for i in x]
        myplot2('awayteam_for_NFL.png', x, y, 'Away', 'blue')
        plt.show()

    # Simiarly, draw for MLB
    else:
        print("Your are interested in: Baseball\n")
        print("This is the overview about the number distribution of every team:")

        def die(s):
            print('[DIE] %s' % s)
            exit()

        home_dict = {}
        away_dict = {}

        for i in csv.reader(open('MLB_data.csv')):
            h = i[1]
            a = i[2]
            if h == 'Home_Team':  # header
                continue
            h = h.split('vs.')
            if len(h) not in [1, 2]:
                die('Invalid Home_Team Data')

            if len(h) == 2:
                if len(a) != 0:
                    die('Invalid Away_Team Data')
                a = h[1]
                h = h[0].split(':')
                if len(h) != 2:
                    die('Invalid Home_Team Data')
                h = h[1]
            else:
                h = h[0]

            h = h.split('(')[0]
            a = a.split('(')[0]
            h = h.split('-')[-1]
            a = a.split('-')[-1]

            if h not in home_dict:
                home_dict[h] = 0
            if a not in away_dict:
                away_dict[a] = 0
            home_dict[h] += 1
            away_dict[a] += 1

        def myplot2(fn, x, y, t, c):
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            ax.barh(x, y, color=c)
            ax.set_xlabel('Number of Tickets', fontsize=8)
            ax.set_title(t, fontsize=15)
            ax.set_ylabel('Team Name', fontsize=8)
            ax.yaxis.set_label_position('right')
            ax.tick_params(labelsize=6, left=False, bottom=False)
            ax.tick_params(axis='x', labelsize=8)
            ax.tick_params(axis='y', pad=0)

        x = list(home_dict.keys())
        y = [home_dict[i] for i in x]
        myplot2('hometeam_for_MLB.png', x, y, 'Home', 'red')

        x = list(away_dict.keys())
        y = [away_dict[i] for i in x]
        myplot2('awayteam_for_MLB.png', x, y, 'Away', 'blue')
        plt.show()

    # Event Filter
    print("\n\n--------------------------------------------------------------------------")
    print("                   ***Event Filter***\n")
    # Choose the team name
    # get all the team names based on the chosen sport

    team_names = pd.concat([data["Home_Team"], data["Away_Team"]])
    team = sorted(list(set(team_names)))
    print("Please choose one team name from the list:\n")
    for i in team:
        print(i)
    # ask the user to input
    team = input("\nTeam name:")
    team = team.lower()
    print("\nThe team you choose is: " + team)
    print('Your search result is:')
    # User chose nothing
    if team == ' ':
        team_data = data
        print(team_data.to_string())
    # Filter the data according to the chosen team name
    else:
        team_data = data
        for i in range(len(data)):
            if team.strip() not in data['Home_Team'][i].lower() and team.strip() not in data['Away_Team'][i].lower():
                team_data = team_data.drop(index=i)
        team_data = team_data.reset_index(drop=True)
        print(team_data.to_string())

    # Choose the city
    # more than one records
    if len(team_data) != 1:
        city = sorted(list(set(team_data['City'])))
        print("\nPlease choose your the city name from the list:\n")
        for i in city:
            print(i)
        # ask the user to input
        city = input("\ncity name: ")

    # If there is only one record after filtering, print that
    if len(team_data) == 1:
        city_data = team_data
    # more than one records
    else:
        print("The city you choose is: " + city)
        print('Your search result is:')
        # Filter the data according to the chosen city name
        if city != ' ':
            try:
                city_data = team_data[team_data['City'].lower() == city.lower()]
                city_data = city_data.reset_index(drop=True)
            except:
                city_data = team_data
        # User chose nothing
        else:
            city_data = team_data
        city_data = city_data.reset_index(drop=True)
        print(city_data.to_string())

    # choose date
    # If there is only one record after filtering, print that
    if len(city_data) == 1:
        print('Your search result after choosing date is:')
        date_data = city_data
        print(city_data.to_string())
    # more than one records
    else:
        date = sorted([i for i in city_data["Date"] if i != 'TBD'])
        print("Choose a date from " + str(date[0])[0:10] + " to " + str(date[-1])[0:10])
        min_date = input("Please enter the start date as YYYY-MM-DD: ")
        max_date = input("Please enter the end date as YYYY-MM-DD: ")

    if len(city_data) > 1:
        if min_date is None:
            min_d = str(date[0])[0:10]
            min_d = datetime.strptime(min_d, "%Y-%m-%d").date()
        if max_date is None:
            max_d = str(date[-1])[0:10]
            max_d = datetime.strptime(max_d, "%Y-%m-%d").date()
        else:
            try:
                min_d = datetime.strptime(min_date, "%Y-%m-%d").date()
                max_d = datetime.strptime(max_date, "%Y-%m-%d").date()
            except:
                print("Wrong Input! Display all from the records above.")
                min_d = str(date[0])[0:10]
                min_d = datetime.strptime(min_d, "%Y-%m-%d").date()
                max_d = str(date[-1])[0:10]
                max_d = datetime.strptime(max_d, "%Y-%m-%d").date()
        if max_d >= min_d:
            print("The date is from: " + str(min_d) + " to " + str(max_d))
            date_data = city_data
            for i in range(len(city_data)):
                if city_data['Date'][i] != 'TBD':
                    try:
                        if city_data['Date'][i] < min_d or city_data['Date'][i] > max_d:
                            date_data = date_data.drop(index=i)
                    except:
                        if datetime.strptime(city_data['Date'][i], "%Y-%m-%d").date() < min_d or datetime.strptime(
                                city_data['Date'][i], "%Y-%m-%d").date() > max_d:
                            date_data = date_data.drop(index=i)
            if len(date_data) > 0:
                print('Your search result is:')
                date_data = date_data.reset_index(drop=True)
                print(date_data.to_string())
            else:
                print("No matches, please re-enter the start and end date.")
        else:
            print("No matches, please re-enter the start and end date.")
    else:
        date_data = date_data.reset_index(drop=True)
        date_data = city_data
        print(city_data.to_string())

    # sort by
    print("\n\n--------------------------------------------------------------------------")
    print("                   *** Sort By***")

    print("Sort By \n")
    option = ["Price low to high", "Price high to low", "Most recently", "Least Recently"]
    for i in option:
        print(i)
    sort = input("Sort by: \n")
    print("\n")
    print("You choice to sort by: " + sort)
    # sort the records
    for i in range(len(date_data)):
        try:
            date_data['Price'][i] = int(date_data['Price'][i][1:].strip())
        except:
            date_data['Price'][i] = 0
    # Price low to high
    if sort == "Price low to high":
        date_data = date_data.sort_values(by=['Price'], ascending=True)
    # Price high to low
    elif sort == "Price high to low":
        date_data = date_data.sort_values(by=['Price'], ascending=False)
    # Most recently
    elif sort == "Most recently":
        date_data1 = date_data[date_data['Date'] != "TBD"]
        date_data1 = date_data1.sort_values(by=['Date'], ascending=True)
        date_data2 = date_data[date_data['Date'] == "TBD"]
        date_data = pd.concat([date_data1, date_data2])
        date_data = date_data.reset_index(drop=True)
    # Least Recently
    elif sort == "Least Recently":
        date_data1 = date_data[date_data['Date'] != "TBD"]
        date_data1 = date_data1.sort_values(by=['Date'], ascending=False)
        date_data2 = date_data[date_data['Date'] == "TBD"]
        date_data = pd.concat([date_data1, date_data2])
        date_data = date_data.reset_index(drop=True)
        # results
    date_data = date_data.reset_index(drop=True)
    print(date_data.to_string())

    # choose the ticket
    print("\n\n--------------------------------------------------------------------------")
    print("                  *** Final Sports Tickets***\n")

    while True:
        print("Please select your final choice by input the index of the tickets: \n")
        print(date_data.to_string())
        choice = input("Your final choice index:")
        try:
            choice = int(choice)
            if choice != ' ':
                date_data = date_data.fillna(0)
                price = date_data['Price'][choice]
                print(
                    "The sports teams are: " + date_data['Home_Team'][choice] + " vs." + date_data['Away_Team'][choice])
                print("The game time is on " + str(date_data['Date'][choice]) + " at " + date_data['Time'][choice])
                print("The ticket price is: $" + str(price))
            break;
        except:
            print("Please make your choice.")
    print("--------------------------------------------------------------------------")
    return date_data, choice, price


# ------------------------------------------------Flight Data Crawler and Input-----------------------------------------


def flight(date_data, choice):
    # ----------------------------------------------IATA code---------------------------------------------
    # Store the iata (airports three letter) code to dictionary
    iata = open('airports.json')
    data_code = json.load(iata)

    # -----------------------------------------Flight scrape function-------------------------------------
    # Take origin iata code, destination iata code, startdate and enddate in YYY-MM-DD format
    # return the results Dataframe

    def scrape(origin, destination, startdate, enddate):

        if origin == '' or destination == '':
            return

        url = "https://www.kayak.com/flights/" + origin + "-" + destination + "/" + startdate + "/" + enddate + "?sort=bestflight_a&fs=stops=0"

        chrome_options = webdriver.ChromeOptions()
        # chrome version used on your device
        agents = ["Chrome/104.0.5112.101"]
        chrome_options.add_argument('--user-agent=' + agents[(requests % len(agents))] + '"')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options,
                                  desired_capabilities=chrome_options.to_capabilities())
        driver.implicitly_wait(20)
        driver.get(url)

        # Check if Kayak thinks that we're a robot
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        if soup.find_all('p')[0].getText() == "Please confirm that you are a real KAYAK user.":
            print("Kayak thinks I'm a bot, let's wait and try again")
            driver.close()
            time.sleep(10)
            return "failure"

        soup = BeautifulSoup(driver.page_source, 'lxml')

        # get the arrival and departure times
        deptimes = soup.find_all('span', attrs={'class': 'depart-time base-time'})
        arrtimes = soup.find_all('span', attrs={'class': 'arrival-time base-time'})
        # am or pm
        meridies = soup.find_all('span', attrs={'class': 'time-meridiem meridiem'})

        deptime = []
        for div in deptimes:
            deptime.append(div.getText()[:-1])

        arrtime = []
        for div in arrtimes:
            arrtime.append(div.getText()[:-1])

        meridiem = []
        for div in meridies:
            meridiem.append(div.getText())

        # reshape them to get origin time and destination time
        deptime = np.asarray(deptime)
        deptime = deptime.reshape(int(len(deptime) / 2), 2)

        arrtime = np.asarray(arrtime)
        arrtime = arrtime.reshape(int(len(arrtime) / 2), 2)

        meridiem = np.asarray(meridiem)
        meridiem = meridiem.reshape(int(len(meridiem) / 4), 4)

        # Get the price

        price_list = soup.find_all('span', attrs={'class': 'price-text'})

        price = []
        for div in price_list:
            price.append(div.text.split('\n')[-1])
        deptime_o = [m + str(n) for m, n in zip(deptime[:, 0], meridiem[:, 0])]
        arrtime_d = [m + str(n) for m, n in zip(arrtime[:, 0], meridiem[:, 1])]
        deptime_d = [m + str(n) for m, n in zip(deptime[:, 1], meridiem[:, 2])]
        arrtime_o = [m + str(n) for m, n in zip(arrtime[:, 1], meridiem[:, 3])]
        df = pd.DataFrame({"origin": [origin for i in range(0, len(deptime_o))],
                           "destination": [destination for i in range(0, len(deptime_o))],
                           "startdate": [startdate for i in range(0, len(deptime_o))],
                           "enddate": [enddate for i in range(0, len(deptime_o))],
                           "price": price[0:len(deptime_o)],
                           "currency": ["USD" for i in range(0, len(deptime_o))],
                           "deptime_origin": deptime_o,
                           "arrtime_destination": arrtime_d,
                           "deptime_destination": deptime_d,
                           "arrtime_origin": arrtime_o
                           })

        driver.close()  # close the browser

        time.sleep(1)

        return df

    # -----------------------------------------------Flight Input----------------------------------------------

    # Get the city name from previous input
    city = date_data['City'][choice]
    # city = 'Philadelphia'

    # Create an empty dataframe
    results = pd.DataFrame(
        columns=['origin', 'destination', 'startdate', 'enddate', 'deptime_origin', 'arrtime_destination',
                 'deptime_destination', 'arrtime_origin',
                 'currency', 'price'])

    requests = 1

    # User input
    origins_input = input('From which city? Please enter the city name ')
    print()
    # print out the airport options in the city
    [print(v['name']) for k, v in data_code.items() if v['city'] == origins_input]
    airport_o = input('Please enter an airport from options above ')
    # get the origin's iata code
    origins = [v['iata'] for k, v in data_code.items() if v['name'] == airport_o]
    print()
    # print out the airport options in the city
    [print(v['name']) for k, v in data_code.items() if v['city'] == city]
    destinations_intput1 = input('Please enter the destination airport from options above ')
    # get the destination's iata code
    destinations = [v['iata'] for k, v in data_code.items() if v['name'] == destinations_intput1]

    startdates = input('Search around which departure date? Please use YYYY-MM-DD format only ')
    # return date
    enddates = input('Search around which return date? Please use YYYY-MM-DD format only ')
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import lxml
import lxml.etree
import re
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import time
import json
from urllib.request import urlopen
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import matplotlib.pyplot as plt


# ------------------------------------------------Sports Data Crawler ----------------------------------------------

def MLB_scrapper_func():
    # MLB Scraper function
    # scrape the MLB data from the stubhub
    import time
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://www.stubhub.com/mlb-tickets")
    driver.implicitly_wait(20)
    time.sleep(10)
    while True:
        # if there is any see more bottun, click it
        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'See More')]").click()
            time.sleep(0.5)
        # else break the loop
        except:
            break
            # scroll down to the end
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_text = driver.page_source
    driver.quit()
    # print(page_text)
    # use BeautifulSoup to read and clean the data
    soup = BeautifulSoup(page_text, 'html.parser')
    span = soup.find_all("span")
    for s in span:
        if "locations" in s.text:
            target = s
    a_s = target.parent.parent.find_all("a")
    # define the elements we want
    date = []
    day = []
    time = []
    home_team = []
    away_team = []
    location = []
    city = []
    states = []
    country = []
    price = []
    cnt = 0
    # clean and get all the information needed
    for a in a_s:
        # remove the season package ticket
        if "TBD at" not in str(a.get_text("[SEP]")):
            tickets = a.time.parent.parent.parent.get_text("[SEP]")
            ticket = tickets.split("[SEP]")
            # find the year
            datetime_object = datetime.strptime(ticket[0][0:3], "%b")
            month_number = datetime_object.month
            currentMonth = datetime.now().month
            # get the date
            if month_number < currentMonth:
                date.append(ticket[0] + ' 23')
            else:
                date.append(ticket[0] + ' 22')
            # day
            day.append(ticket[1])
            # time
            time.append(ticket[2])
            # team names
            t = ticket[3].split(':')
            t = t[0].split('at ')
            if len(t) > 1:
                home_team.append(t[1].strip())
                away_team.append(t[0].strip())
            else:
                home_team.append(pd.NA)
                away_team.append(pd.NA)
                # location
            loc = ticket[4].split(", ")
            if len(loc) == 4:
                if "TBD" in loc[0]:
                    sta = loc[0].split("TBD -\xa0")
                    location.append(sta[1])
                    city.append(loc[1])
                    states.append(loc[2])
                    country.append(loc[3])
                else:
                    location.append(loc[0])
                    city.append(loc[1])
                    states.append(loc[2])
                    country.append(loc[3])
            elif len(loc) == 3:
                if "TBD" in loc[0]:
                    sta = loc[0].split("TBD -\xa0")
                    location.append(sta[1])
                    city.append(loc[1])
                    states.append('')
                    country.append(loc[2])
                else:
                    location.append(loc[0])
                    city.append(loc[1])
                    states.append('')
                    country.append(loc[2])
                    # price
            if ticket[-1].startswith('$'):
                price.append(ticket[-1])
            elif ticket[-4].startswith('$'):
                price.append(ticket[-4])
            else:
                price.append(pd.NA)
    # get the final dataframe
    data = list(zip(home_team, away_team, location, city, states, country, date, day, time, price))
    data = pd.DataFrame(data,
                        columns=['Home_Team', 'Away_Team', 'Arena', 'City', 'State', 'Country', 'Date', 'Day', 'Time',
                                 'Price'])
    data["Home_Team"] = data["Home_Team"].replace(r'^\s*$', np.nan, regex=True)
    data["Away_Team"] = data["Away_Team"].replace(r'^\s*$', np.nan, regex=True)
    for i in range(len(data)):
        if data["Date"][i] != "TBD":
            data["Date"][i] = datetime.strptime(data["Date"][i], "%b %d %y")
            data["Date"][i] = datetime.strftime(data["Date"][i], "%Y-%m-%d")
            data["Date"][i] = datetime.strptime(data["Date"][i], "%Y-%m-%d").date()
        if data["Home_Team"][i] == np.nan or data["Away_Team"][i] == np.nan:
            data = data.drop(index=i)
    MLB_data = data.reset_index(drop=True)
    print("                    ***MLB Data***")
    print("------------------------------------------------------------")
    print(MLB_data)
    MLB_data.to_csv('./MLB_data.csv')
    return MLB_data


# ------------------------------------------------Sports Data Crawler ----------------------------------------------

def NFL_scrapper_func():
    # NFL Scraper function
    # scrape the NFL data from the stubhub
    import time
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(
        "https://www.stubhub.com/nfl-tickets/?gcid=C12289X486&utm_source=google&utm_medium=paid-search&utm_sub_medium=prospecting&utm_term=tm&utm_campaign=33820630%3Adefault&utm_content=default&keyword=1160920960_kwd-113741604_c&creative=249920920219&utm_kxconfid=s2rshsbmv&kwt=tm&mt=e&kw=stubhub&MetroRegionID=&psc=&ps=&ps_p=0&ps_c=33820630&ps_ag=1160920960&ps_tg=kwd-113741604&ps_ad=249920920219&ps_adp=&ps_fi=&ps_li=&ps_lp=9005925&ps_n=g&ps_d=c&PCID=PSUSGOOSHGBR56BB04400F&gclid=Cj0KCQjwmouZBhDSARIsALYcouooEqqgILz8he7beWGMZaL1vodi8XfPGqZASsqYGC3Tv0WHfKVHqAYaAiQOEALw_wcB&gridFilterType=0")
    driver.implicitly_wait(30)
    time.sleep(10)
    while True:
        # if there is any see more bottun, click it
        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'See More')]").click()
        # else break the loop
        except:
            break
            # scroll down to the end
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_text = driver.page_source

    driver.quit()
    # print(page_text)
    # use BeautifulSoup to read and clean the data
    soup = BeautifulSoup(page_text, 'html.parser')
    span = soup.find_all("span")
    for s in span:
        if "locations" in s.text:
            target = s
    a_s = target.parent.parent.find_all("a")
    # define the elements we want
    date = []
    day = []
    time = []
    home_team = []
    away_team = []
    location = []
    city = []
    states = []
    country = []
    price = []
    cnt = 0
    # clean and get all the information needed
    for a in a_s:
        # remove the season package ticket
        if "TBD" not in str(a.get_text("[SEP]")) and "Tailgate Party " not in str(a.get_text("[SEP]")):
            try:
                tickets = a.time.parent.parent.parent.get_text("[SEP]")
                ticket = tickets.split("[SEP]")
                # find the year
                datetime_object = datetime.strptime(ticket[0][0:3], "%b")
                month_number = datetime_object.month
                currentMonth = datetime.now().month
                # get the date
                if month_number < currentMonth:
                    date.append(ticket[0] + ' 23')
                else:
                    date.append(ticket[0] + ' 22')
                # day
                day.append(ticket[1])
                # time
                time.append(ticket[2])
                # team names
                t = ticket[3].split(':')
                t = t[0].split('at ')
                if len(t) > 1:
                    home_team.append(t[1].strip())
                    away_team.append(t[0].strip())
                else:
                    home_team.append(pd.NA)
                    away_team.append(pd.NA)
                    # location
                loc = ticket[4].split(", ")
                if len(loc) == 4:
                    if "TBD" in loc[0]:
                        sta = loc[0].split("TBD -\xa0")
                        location.append(sta[1])
                        city.append(loc[1])
                        states.append(loc[2])
                        country.append(loc[3])
                    else:
                        location.append(loc[0])
                        city.append(loc[1])
                        states.append(loc[2])
                        country.append(loc[3])
                elif len(loc) == 3:
                    if "TBD" in loc[0]:
                        sta = loc[0].split("TBD -\xa0")
                        location.append(sta[1])
                        city.append(loc[1])
                        states.append('')
                        country.append(loc[2])
                    else:
                        location.append(loc[0])
                        city.append(loc[1])
                        states.append('')
                        country.append(loc[2])
                        # price
                if ticket[-1].startswith('$'):
                    price.append(ticket[-1])
                elif ticket[-4].startswith('$'):
                    price.append(ticket[-4])
                else:
                    price.append(pd.NA)
            except:
                continue
    # get the final dataframe
    data = list(zip(home_team, away_team, location, city, states, country, date, day, time, price))
    data = pd.DataFrame(data,
                        columns=['Home_Team', 'Away_Team', 'Arena', 'City', 'State', 'Country', 'Date', 'Day', 'Time',
                                 'Price'])
    data["Home_Team"] = data["Home_Team"].replace(r'^\s*$', np.nan, regex=True)
    data["Away_Team"] = data["Away_Team"].replace(r'^\s*$', np.nan, regex=True)
    for i in range(len(data)):
        if data["Date"][i] != "TBD":
            data["Date"][i] = datetime.strptime(data["Date"][i], "%b %d %y")
            data["Date"][i] = datetime.strftime(data["Date"][i], "%Y-%m-%d")
            data["Date"][i] = datetime.strptime(data["Date"][i], "%Y-%m-%d").date()
        if data["Home_Team"].isna()[i] or data["Away_Team"].isna()[i]:
            data = data.drop(index=i)
    NFL_data = data.reset_index(drop=True)
    print("                    ***NFL Data***")
    print("------------------------------------------------------------")
    print(NFL_data)
    NFL_data.to_csv('./NFL_data.csv')
    return NFL_data


# ------------------------------------------------Sports Data Crawler ----------------------------------------------

def NBA_scrapper_func():
    # NBA Scraper function
    # scrape the NBA data from the stubhub
    import time
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.stubhub.com/nba-tickets/grouping/115/")
    driver.implicitly_wait(30)
    time.sleep(10)
    while True:
        # if there is any see more bottun, click it
        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'See More')]").click()
            time.sleep(1)
        # else break the loop
        except:
            break
            # scroll down to the end
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_text = driver.page_source
    driver.quit()
    # print(page_text)
    # use BeautifulSoup to read and clean the data
    soup = BeautifulSoup(page_text, 'html.parser')
    span = soup.find_all("span")
    for s in span:
        if "location" in s.text:
            target = s
    a_s = target.parent.parent.find_all("a")
    # define the elements we want
    date = []
    day = []
    time = []
    home_team = []
    away_team = []
    location = []
    city = []
    states = []
    country = []
    price = []
    cnt = 0
    # clean and get all the information needed
    for a in a_s:
        # remove the season package ticket
        if "Season Package" not in str(a.get_text("[SEP]")):
            tickets = a.time.parent.parent.parent.get_text("[SEP]")
            ticket = tickets.split("[SEP]")
            # find the year
            datetime_object = datetime.strptime(ticket[0][0:3], "%b")
            month_number = datetime_object.month
            currentMonth = datetime.now().month
            # get the date
            if month_number < currentMonth:
                date.append(ticket[0] + ' 23')
            else:
                date.append(ticket[0] + ' 22')
            # day
            day.append(ticket[1])
            # time
            time.append(ticket[2])
            # team names

            if "Preseason" not in ticket[3]:
                t = ticket[3].split('at ')
                if len(t) > 1:
                    home_team.append(t[1].strip())
                    away_team.append(t[0].strip())
            else:
                t = ticket[3].split('at ')
                if len(t) > 1:
                    if "Preseason" in t[1]:
                        home_team.append(t[1].strip())
                        away_team.append(t[0].strip() + " Preseason")
                    else:
                        home_team.append(t[1].strip() + " Preseason")
                        away_team.append(t[0].strip())

                        # location
            loc = ticket[4].split(", ")
            if len(loc) == 4:
                if "TBD" in loc[0]:
                    sta = loc[0].split("TBD -\xa0")
                    location.append(sta[1])
                    city.append(loc[1])
                    states.append(loc[2])
                    country.append(loc[3])
                else:
                    location.append(loc[0])
                    city.append(loc[1])
                    states.append(loc[2])
                    country.append(loc[3])
            elif len(loc) == 3:
                if "TBD" in loc[0]:
                    sta = loc[0].split("TBD -\xa0")
                    location.append(sta[1])
                    city.append(loc[1])
                    states.append('')
                    country.append(loc[2])
                else:
                    location.append(loc[0])
                    city.append(loc[1])
                    states.append('')
                    country.append(loc[2])
                    # price
            if ticket[-1].startswith('$'):
                price.append(ticket[-1])
            else:
                price.append(' ')
    # get the final dataframe
    data = list(zip(home_team, away_team, location, city, states, country, date, day, time, price))
    data = pd.DataFrame(data,
                        columns=['Home_Team', 'Away_Team', 'Arena', 'City', 'State', 'Country', 'Date', 'Day', 'Time',
                                 'Price'])
    # change the date type
    data["Home_Team"] = data["Home_Team"].replace(r'^\s*$', np.nan, regex=True)
    data["Away_Team"] = data["Away_Team"].replace(r'^\s*$', np.nan, regex=True)
    for i in range(len(data)):
        if data["Date"][i] != "TBD":
            data["Date"][i] = datetime.strptime(data["Date"][i], "%b %d %y")
            data["Date"][i] = datetime.strftime(data["Date"][i], "%Y-%m-%d")
            data["Date"][i] = datetime.strptime(data["Date"][i], "%Y-%m-%d").date()
        if data["Home_Team"].isna()[i] or data["Away_Team"].isna()[i]:
            data = data.drop(index=i)
    NBA_data = data.reset_index(drop=True)
    print("                    ***NBA Data***")
    print("------------------------------------------------------------")
    print(NBA_data)
    # export to csv file
    NBA_data.to_csv('./NBA_data.csv')
    return NBA_data


# ------------------------------------------------Sports Data Input ----------------------------------------------

def sports():
    # call the scraper functions

    # live scraper

    # Due to the UI design of Stubhub
    # Somtimes, the prices cannot display on the front page
    # For convience, if there are no prices
    # choose to use prvious scraped data
    # mlb_data = MLB_scrapper_func()
    # try:
    #     price = int(mlb_data['Price'][0])
    # except:
    #     mlb_data = pd.read_csv("MLB_data_original.csv")
    # nfl_data = NFL_scrapper_func()
    # try:
    #     price = int(nfl_data['Price'][0])
    # except:
    #     nfl_data = pd.read_csv("NFL_data_original.csv")
    # nba_data = NBA_scrapper_func()
    # try:
    #     price = int(nba_data['Price'][0])
    # except:
    #     nba_data = pd.read_csv("NBA_data_original.csv")

    # used privious data directly

    # if you want to use the previous data, you can use this section and you need to comment out the scraper function above
    mlb_data = pd.read_csv("MLB_data_original.csv")

    nfl_data = pd.read_csv("NFL_data_original.csv")

    nba_data = pd.read_csv("NBA_data_original.csv")

    print("                   ***Sports Tickets***")
    print("--------------------------------------------------------------------------\n")
    while True:
        sport = input("Please choose the sports name from NBA, NFL, MLB\n")
        if sport.upper() == 'NBA':
            print("Your choice is: " + sport)
            data_new = nba_data
            button = 1
            break;
        elif sport.upper() == 'NFL':
            print("Your choice is: " + sport)
            data_new = nfl_data
            button = 2
            break;
        elif sport.upper() == 'MLB':
            print("Your choice is: " + sport)
            data_new = mlb_data
            button = 3
            break;
        else:
            continue
    data = data_new
    print(data.to_string())
    print("\n\n--------------------------------------------------------------------------")
    print("                   ***Event Overview***\n")
    # Event Overview
    # Based on the sports selection, show the number of tickets for repsective teams
    # NBA team information generation
    if button == 1:
        print("Your are interested in: Basketball\n")
        print("This is the overview about the number distribution of every team:")

        def die(s):
            print('[DIE] %s' % s)
            exit()

        # Two plots: one for home_team, one for away_team
        home_dict = {}
        away_dict = {}

        for i in csv.reader(open('NBA_data.csv')):
            h = i[1]
            a = i[2]
            if h == 'Home_Team':  # header
                continue

            # Split the String to get the home_team and away_team name, get rid of invalid data
            h = h.split('vs.')
            if len(h) not in [1, 2]:
                die('Invalid Home_Team Data')

            if len(h) == 2:
                if len(a) != 0:
                    die('Invalid Away_Team Data')
                a = h[1]
                h = h[0].split(':')
                if len(h) != 2:
                    die('Invalid Home_Team Data')
                h = h[1]
            else:
                h = h[0]

            h = h.split('(')[0]
            a = a.split('(')[0]
            h = h.split('-')[-1]
            a = a.split('-')[-1]

            # Create dictionary for home_team/away_team and count the ticket amount
            if h not in home_dict:
                home_dict[h] = 0
            if a not in away_dict:
                away_dict[a] = 0
            home_dict[h] += 1
            away_dict[a] += 1

        # Draw the plots
        def myplot2(fn, x, y, t, c):
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            ax.barh(x, y, color=c)
            ax.set_xlabel('Number of Tickets', fontsize=8)
            ax.set_title(t, fontsize=15)
            ax.set_ylabel('Team Name', fontsize=8)
            ax.yaxis.set_label_position('right')
            ax.tick_params(labelsize=6, left=False, bottom=False)
            ax.tick_params(axis='x', labelsize=8)
            ax.tick_params(axis='y', pad=0)

        x = list(home_dict.keys())
        y = [home_dict[i] for i in x]
        myplot2('hometeam_for_NBA.png', x, y, 'Home', 'red')

        x = list(away_dict.keys())
        y = [away_dict[i] for i in x]
        myplot2('awayteam_for_NBA.png', x, y, 'Away', 'blue')
        plt.show()

    # Similarly, draw for NFL
    elif button == 2:
        print("Your are interested in: Football\n")
        print("This is the overview about the number distribution of every team:")

        def die(s):
            print('[DIE] %s' % s)
            exit()

        home_dict = {}
        away_dict = {}

        for i in csv.reader(open('NFL_data.csv')):
            h = i[1]
            a = i[2]
            if h == 'Home_Team':  # header
                continue
            h = h.split('vs.')
            if len(h) not in [1, 2]:
                die('Invalid Home_Team Data')

            if len(h) == 2:
                if len(a) != 0:
                    die('Invalid Away_Team Data')
                a = h[1]
                h = h[0].split(':')
                if len(h) != 2:
                    die('Invalid Home_Team Data')
                h = h[1]
            else:
                h = h[0]

            h = h.split('(')[0]
            a = a.split('(')[0]
            h = h.split('-')[-1]
            a = a.split('-')[-1]

            if h not in home_dict:
                home_dict[h] = 0
            if a not in away_dict:
                away_dict[a] = 0
            home_dict[h] += 1
            away_dict[a] += 1

        def myplot2(fn, x, y, t, c):
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            ax.barh(x, y, color=c)
            ax.set_xlabel('Number of Tickets', fontsize=8)
            ax.set_title(t, fontsize=15)
            ax.set_ylabel('Team Name', fontsize=8)
            ax.yaxis.set_label_position('right')
            ax.tick_params(labelsize=6, left=False, bottom=False)
            ax.tick_params(axis='x', labelsize=8)
            ax.tick_params(axis='y', pad=0)

        x = list(home_dict.keys())
        y = [home_dict[i] for i in x]
        myplot2('hometeam_for_NFL.png', x, y, 'Home', 'red')

        x = list(away_dict.keys())
        y = [away_dict[i] for i in x]
        myplot2('awayteam_for_NFL.png', x, y, 'Away', 'blue')
        plt.show()

    # Simiarly, draw for MLB
    else:
        print("Your are interested in: Baseball\n")
        print("This is the overview about the number distribution of every team:")

        def die(s):
            print('[DIE] %s' % s)
            exit()

        home_dict = {}
        away_dict = {}

        for i in csv.reader(open('MLB_data.csv')):
            h = i[1]
            a = i[2]
            if h == 'Home_Team':  # header
                continue
            h = h.split('vs.')
            if len(h) not in [1, 2]:
                die('Invalid Home_Team Data')

            if len(h) == 2:
                if len(a) != 0:
                    die('Invalid Away_Team Data')
                a = h[1]
                h = h[0].split(':')
                if len(h) != 2:
                    die('Invalid Home_Team Data')
                h = h[1]
            else:
                h = h[0]

            h = h.split('(')[0]
            a = a.split('(')[0]
            h = h.split('-')[-1]
            a = a.split('-')[-1]

            if h not in home_dict:
                home_dict[h] = 0
            if a not in away_dict:
                away_dict[a] = 0
            home_dict[h] += 1
            away_dict[a] += 1

        def myplot2(fn, x, y, t, c):
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            ax.barh(x, y, color=c)
            ax.set_xlabel('Number of Tickets', fontsize=8)
            ax.set_title(t, fontsize=15)
            ax.set_ylabel('Team Name', fontsize=8)
            ax.yaxis.set_label_position('right')
            ax.tick_params(labelsize=6, left=False, bottom=False)
            ax.tick_params(axis='x', labelsize=8)
            ax.tick_params(axis='y', pad=0)

        x = list(home_dict.keys())
        y = [home_dict[i] for i in x]
        myplot2('hometeam_for_MLB.png', x, y, 'Home', 'red')

        x = list(away_dict.keys())
        y = [away_dict[i] for i in x]
        myplot2('awayteam_for_MLB.png', x, y, 'Away', 'blue')
        plt.show()

    # Event Filter
    print("\n\n--------------------------------------------------------------------------")
    print("                   ***Event Filter***\n")
    # Choose the team name
    # get all the team names based on the chosen sport

    team_names = pd.concat([data["Home_Team"], data["Away_Team"]])
    team = sorted(list(set(team_names)))
    print("Please choose one team name from the list:\n")
    for i in team:
        print(i)
    # ask the user to input
    team = input("\nTeam name:")
    team = team.lower()
    print("\nThe team you choose is: " + team)
    print('Your search result is:')
    # User chose nothing
    if team == ' ':
        team_data = data
        print(team_data.to_string())
    # Filter the data according to the chosen team name
    else:
        team_data = data
        for i in range(len(data)):
            if team.strip() not in data['Home_Team'][i].lower() and team.strip() not in data['Away_Team'][i].lower():
                team_data = team_data.drop(index=i)
        team_data = team_data.reset_index(drop=True)
        print(team_data.to_string())

    # Choose the city
    # more than one records
    if len(team_data) != 1:
        city = sorted(list(set(team_data['City'])))
        print("\nPlease choose your the city name from the list:\n")
        for i in city:
            print(i)
        # ask the user to input
        city = input("\ncity name: ")

    # If there is only one record after filtering, print that
    if len(team_data) == 1:
        city_data = team_data
    # more than one records
    else:
        print("The city you choose is: " + city)
        print('Your search result is:')
        # Filter the data according to the chosen city name
        if city != ' ':
            try:
                city_data = team_data[team_data['City'] == city]
                city_data = city_data.reset_index(drop=True)
            except:
                city_data = team_data
        # User chose nothing
        else:
            city_data = team_data
        city_data = city_data.reset_index(drop=True)
        print(city_data.to_string())

    # choose date
    # If there is only one record after filtering, print that
    if len(city_data) == 1:
        print('Your search result after choosing date is:')
        date_data = city_data
        print(city_data.to_string())
    # more than one records
    else:
        date = sorted([i for i in city_data["Date"] if i != 'TBD'])
        print("Choose a date from " + str(date[0])[0:10] + " to " + str(date[-1])[0:10])
        min_date = input("Please enter the start date as YYYY-MM-DD: ")
        max_date = input("Please enter the end date as YYYY-MM-DD: ")

    if len(city_data) > 1:
        if min_date is None:
            min_d = str(date[0])[0:10]
            min_d = datetime.strptime(min_d, "%Y-%m-%d").date()
        if max_date is None:
            max_d = str(date[-1])[0:10]
            max_d = datetime.strptime(max_d, "%Y-%m-%d").date()
        else:
            try:
                min_d = datetime.strptime(min_date, "%Y-%m-%d").date()
                max_d = datetime.strptime(max_date, "%Y-%m-%d").date()
            except:
                print("Wrong Input! Display all from the records above.")
                min_d = str(date[0])[0:10]
                min_d = datetime.strptime(min_d, "%Y-%m-%d").date()
                max_d = str(date[-1])[0:10]
                max_d = datetime.strptime(max_d, "%Y-%m-%d").date()
        if max_d >= min_d:
            print("The date is from: " + str(min_d) + " to " + str(max_d))
            date_data = city_data
            for i in range(len(city_data)):
                if city_data['Date'][i] != 'TBD':
                    try:
                        if city_data['Date'][i] < min_d or city_data['Date'][i] > max_d:
                            date_data = date_data.drop(index=i)
                    except:
                        if datetime.strptime(city_data['Date'][i], "%Y-%m-%d").date() < min_d or datetime.strptime(
                                city_data['Date'][i], "%Y-%m-%d").date() > max_d:
                            date_data = date_data.drop(index=i)
            if len(date_data) > 0:
                print('Your search result is:')
                date_data = date_data.reset_index(drop=True)
                print(date_data.to_string())
            else:
                print("No matches, please re-enter the start and end date.")
        else:
            print("No matches, please re-enter the start and end date.")
    else:
        date_data = date_data.reset_index(drop=True)
        date_data = city_data
        print(city_data.to_string())

    # sort by
    print("\n\n--------------------------------------------------------------------------")
    print("                   *** Sort By***")

    print("Sort By \n")
    option = ["Price low to high", "Price high to low", "Most recently", "Least Recently"]
    for i in option:
        print(i)
    sort = input("Sort by: \n")
    print("\n")
    print("You choice to sort by: " + sort)
    # sort the records
    for i in range(len(date_data)):
        try:
            date_data['Price'][i] = int(date_data['Price'][i][1:].strip())
        except:
            date_data['Price'][i] = 0
    # Price low to high
    if sort == "Price low to high":
        date_data = date_data.sort_values(by=['Price'], ascending=True)
    # Price high to low
    elif sort == "Price high to low":
        date_data = date_data.sort_values(by=['Price'], ascending=False)
    # Most recently
    elif sort == "Most recently":
        date_data1 = date_data[date_data['Date'] != "TBD"]
        date_data1 = date_data1.sort_values(by=['Date'], ascending=True)
        date_data2 = date_data[date_data['Date'] == "TBD"]
        date_data = pd.concat([date_data1, date_data2])
        date_data = date_data.reset_index(drop=True)
    # Least Recently
    elif sort == "Least Recently":
        date_data1 = date_data[date_data['Date'] != "TBD"]
        date_data1 = date_data1.sort_values(by=['Date'], ascending=False)
        date_data2 = date_data[date_data['Date'] == "TBD"]
        date_data = pd.concat([date_data1, date_data2])
        date_data = date_data.reset_index(drop=True)
        # results
    date_data = date_data.reset_index(drop=True)
    print(date_data.to_string())

    # choose the ticket
    print("\n\n--------------------------------------------------------------------------")
    print("                  *** Final Sports Tickets***\n")

    while True:
        print("Please select your final choice by input the index of the tickets: \n")
        print(date_data.to_string())
        choice = input("Your final choice index:")
        try:
            choice = int(choice)
            if choice != ' ':
                date_data = date_data.fillna(0)
                price = date_data['Price'][choice]
                print(
                    "The sports teams are: " + date_data['Home_Team'][choice] + " vs." + date_data['Away_Team'][choice])
                print("The game time is on " + str(date_data['Date'][choice]) + " at " + date_data['Time'][choice])
                print("The ticket price is: $" + str(price))
            break;
        except:
            print("Please make your choice.")
    date_data = date_data.reset_index(drop=True)
    print("--------------------------------------------------------------------------")
    return date_data, choice, price


# ------------------------------------------------Flight Data Crawler and Input-----------------------------------------


def flight(date_data, choice):
    # ----------------------------------------------IATA code---------------------------------------------
    # Store the iata (airports three letter) code to dictionary
    iata = open('airports.json')
    data_code = json.load(iata)

    # -----------------------------------------Flight scrape function-------------------------------------
    # Take origin iata code, destination iata code, startdate and enddate in YYY-MM-DD format
    # return the results Dataframe

    def scrape(origin, destination, startdate, enddate):

        if origin == '' or destination == '':
            return

        url = "https://www.kayak.com/flights/" + origin + "-" + destination + "/" + startdate + "/" + enddate + "?sort=bestflight_a&fs=stops=0"

        chrome_options = webdriver.ChromeOptions()
        # chrome version used on your device
        agents = ["Chrome/104.0.5112.101"]
        chrome_options.add_argument('--user-agent=' + agents[(requests % len(agents))] + '"')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options,
                                  desired_capabilities=chrome_options.to_capabilities())
        driver.implicitly_wait(20)
        driver.get(url)

        # Check if Kayak thinks that we're a robot
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        if soup.find_all('p')[0].getText() == "Please confirm that you are a real KAYAK user.":
            print("Kayak thinks I'm a bot, let's wait and try again")
            driver.close()
            time.sleep(10)
            return "failure"

        soup = BeautifulSoup(driver.page_source, 'lxml')

        # get the arrival and departure times
        deptimes = soup.find_all('span', attrs={'class': 'depart-time base-time'})
        arrtimes = soup.find_all('span', attrs={'class': 'arrival-time base-time'})
        # am or pm
        meridies = soup.find_all('span', attrs={'class': 'time-meridiem meridiem'})

        deptime = []
        for div in deptimes:
            deptime.append(div.getText()[:-1])

        arrtime = []
        for div in arrtimes:
            arrtime.append(div.getText()[:-1])

        meridiem = []
        for div in meridies:
            meridiem.append(div.getText())

        # reshape them to get origin time and destination time
        deptime = np.asarray(deptime)
        deptime = deptime.reshape(int(len(deptime) / 2), 2)

        arrtime = np.asarray(arrtime)
        arrtime = arrtime.reshape(int(len(arrtime) / 2), 2)

        meridiem = np.asarray(meridiem)
        meridiem = meridiem.reshape(int(len(meridiem) / 4), 4)

        # Get the price

        price_list = soup.find_all('span', attrs={'class': 'price-text'})

        price = []
        for div in price_list:
            price.append(div.text.split('\n')[-1])
        deptime_o = [m + str(n) for m, n in zip(deptime[:, 0], meridiem[:, 0])]
        arrtime_d = [m + str(n) for m, n in zip(arrtime[:, 0], meridiem[:, 1])]
        deptime_d = [m + str(n) for m, n in zip(deptime[:, 1], meridiem[:, 2])]
        arrtime_o = [m + str(n) for m, n in zip(arrtime[:, 1], meridiem[:, 3])]
        df = pd.DataFrame({"origin": [origin for i in range(0, len(deptime_o))],
                           "destination": [destination for i in range(0, len(deptime_o))],
                           "startdate": [startdate for i in range(0, len(deptime_o))],
                           "enddate": [enddate for i in range(0, len(deptime_o))],
                           "price": price[0:len(deptime_o)],
                           "currency": ["USD" for i in range(0, len(deptime_o))],
                           "deptime_origin": deptime_o,
                           "arrtime_destination": arrtime_d,
                           "deptime_destination": deptime_d,
                           "arrtime_origin": arrtime_o
                           })

        driver.close()  # close the browser

        time.sleep(1)

        return df

    # -----------------------------------------------Flight Input----------------------------------------------

    # Get the city name from previous input
    city = date_data['City'][choice]
    # city = 'Philadelphia'

    # Create an empty dataframe
    results = pd.DataFrame(
        columns=['origin', 'destination', 'startdate', 'enddate', 'deptime_origin', 'arrtime_destination',
                 'deptime_destination', 'arrtime_origin',
                 'currency', 'price'])

    requests = 1

    # User input
    origins_input = input('From which city? Please enter the city name ')
    print()
    # print out the airport options in the city
    [print(v['name']) for k, v in data_code.items() if v['city'] == origins_input]
    airport_o = input('Please enter an airport from options above ')
    # get the origin's iata code
    origins = [v['iata'] for k, v in data_code.items() if v['name'] == airport_o]
    print()
    # print out the airport options in the city
    [print(v['name']) for k, v in data_code.items() if v['city'] == city]
    destinations_intput1 = input('Please enter the destination airport from options above ')
    # get the destination's iata code
    destinations = [v['iata'] for k, v in data_code.items() if v['name'] == destinations_intput1]

    startdates = input('Search around which departure date? Please use YYYY-MM-DD format only ')
    # return date
    enddates = input('Search around which return date? Please use YYYY-MM-DD format only ')

    # scrape flight data
    for origin in origins:
        for destination in destinations:
            results = pd.concat([results, scrape(origin, destination, startdates, enddates)])

    # -------------------------------------Flight Results--------------------------------------------------
    print()
    print('The cheapest options: ')
    print(results[results.price == results.price.min()].to_string())
    print('All possible flights: ')
    print(results.to_string())
    index = int(input('Please enter the flight row number that you want: '))
    flight_price1 = results.loc[index, 'price']
    # get the flight price chose by user
    flight_price1 = int(flight_price1.split('$')[1])
    departure_date1 = results.loc[index, 'startdate']
    return_date1 = results.loc[index, 'enddate']
    departure_time_o1 = results.loc[index, 'deptime_origin']
    departure_time_d1 = results.loc[index, 'deptime_destination']
    return flight_price1, departure_date1, return_date1, departure_time_o1, departure_time_d1, destinations_intput1, airport_o

# ------------------------------------------------Yelp Data and Recommendation-----------------------------------------

def yelp():
    # business_json_path = 'yelp_academic_dataset_business.json'
    # df_b = pd.read_json(business_json_path, lines=True)
    #
    # df_b = df_b[df_b['is_open']==1]
    # drop_columns = ['hours','is_open','review_count']
    # df_b = df_b.drop(drop_columns, axis=1)
    #
    # business_RV = df_b[df_b['categories'].str.contains(
    #               'RV Repair|RV Dealers|RV Rental|RV Parks|Campgrounds',
    #               case=False, na=False)]
    #
    # df_explode = df_b.assign(categories = df_b.categories
    #                          .str.split(', ')).explode('categories')
    # df_explode.categories.value_counts()
    # df_explode[df_explode.categories.str.contains('RV',
    #                       case=True,na=False)].categories.value_counts()
    #
    # review_json_path = 'yelp_academic_dataset_review.json'
    # size = 1000000
    # review = pd.read_json(review_json_path, lines=True,
    #                       dtype={'review_id':str,'user_id':str,
    #                              'business_id':str,'stars':int,
    #                              'date':str,'text':str,'useful':int,
    #                              'funny':int,'cool':int},
    #                       chunksize=size)
    #
    # chunk_list = []
    # for chunk_review in review:
    #     # Drop columns that aren't needed
    #     chunk_review = chunk_review.drop(['review_id','useful','funny','cool'], axis=1)
    #     # Renaming column name to avoid conflict with business overall star rating
    #     chunk_review = chunk_review.rename(columns={'stars': 'review_stars'})
    #     # Inner merge with edited business file so only reviews related to the business remain
    #     chunk_merged = pd.merge(business_RV, chunk_review, on='business_id', how='inner')
    #     # Show feedback on progress
    #     print(f"{chunk_merged.shape[0]} out of {size:,} related reviews")
    #     chunk_list.append(chunk_merged)
    # # After trimming down the review file, concatenate all relevant data back to one dataframe
    # df = pd.concat(chunk_list, ignore_index=True, join='outer', axis=0)
    #
    # csv_name = "yelp_reviews_RV_categories.csv"
    # df.to_csv(csv_name, index=False)
    
    # you can use this csv file directly if you want to save time
    df_event = pd.read_csv('yelp_reviews_RV_categories.csv', usecols= ['state', 'city','address', 'name', 'stars', 'text'], index_col= 'state')
    df_event = df_event.groupby('state').apply(lambda x: x.sort_values(['stars'],ascending = False))
    df_event = df_event.drop_duplicates(['name'])

    # state recommendation
    state_input = input('Please enter the state code: ')
    recommendation = df_event.loc[state_input].head(5)
    return recommendation

    # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    date_data1, choices, prices = sports()

    flight_price, departure_date, return_date, departure_time_o, departure_time_d, destinations_intput, airport_o1 = flight(
        date_data1, choices)
    
    recommendation = yelp()

    # -------------------------------------------------Total Budget------------------------------------------------

    print("The sports teams are: " + date_data1['Home_Team'][choices] + " vs." + date_data1['Away_Team'][choices])
    print("The game time is on " + str(date_data1['Date'][choices]) + " at " + date_data1['Time'][choices])
    print('Your ticket price is: $' + str(prices))
    print('Your flight price is: $' + str(flight_price))
    print('You will depart on ' + departure_date + ' ' + departure_time_o + ' from ' + airport_o1
          + ', return on ' + return_date + ' ' + departure_time_d + ' from ' + destinations_intput)
    print('Your total is :' + str(prices + flight_price))
    print('Here is the recommended event for you: ')
    print(recommendation.to_string())
    print('Bon Voyage!')
 


# In[ ]:





import requests
from bs4 import BeautifulSoup
import traceback
import properties
import time
from datetime import datetime, timedelta
import utility
base_url = "https://www.dotabuff.com/"
extraction_data = {}
matches_list = []

# Extracting the match data
def extract_match_data(match_id):
    try:
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        html_content = requests.get("".join(base_url + "/matches/" + match_id), headers=header)
        return html_content
    except ConnectionError:
        print("There are been connection error")
        print(traceback.print_exc())


def extract_player_infos(player_id):
    try:
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        html_content = requests.get("".join(base_url + "/players/" + player_id), headers=header)
        return html_content
    except ConnectionError:
        print("There are been connection error")
        print(traceback.print_exc())

def player_info():
    players_dict = {}
    for player in properties.player_ids:
        temp_player = {}
        temp_player_data = extract_player_infos(player)
        html_soup = BeautifulSoup(temp_player_data.content, "html.parser")
        player_name = html_soup.find("img", {"class":"image-player"}).get("alt")
        player_image = html_soup.find("img", {"class":"image-player"}).get("src")
        temp_player["name"] = player_name
        temp_player["image_url"] = player_image
        players_dict[player] = temp_player
        time.sleep(20)
    return players_dict


def extract_match_infos():
    try:
        header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        html_content = requests.get("".join(properties.match_id_url), headers=header)
        return html_content

    except ConnectionError:
        print("There are been connection error")
        print(traceback.print_exc())


def calculate_days(date_times):
    filter_dates = []
    for date_time in date_times:
        date = int(date_time.split("-")[2])
        month = int(date_time.split("-")[1])
        year = int(date_time.split("-")[0])
        temp_date = datetime(year, month, date)
        if "," in str(datetime.today() - temp_date):
            diff = int(str(datetime.today() - temp_date).split(" ")[0])
        else:
            diff = 0
        if diff <= properties.days_lookup:
            filter_dates.append(date_time)
    return filter_dates


def populate_match_ids():
    html_content = extract_match_infos()
    html_soup = BeautifulSoup(html_content.content, "html.parser")
    times_list = html_soup.find_all("time")
    date_times = []
    for time1 in times_list:
        if time1["datetime"] not in date_times:
            date_times.append(time1["datetime"])
    date_times = [times.split("T")[0] for times in date_times]
    filter_dates = calculate_days(date_times)
    if filter_dates:
        num_matches = len(filter_dates) - 1
        all_matches = html_soup.find_all("td", {"class":"cell-large"})
        match_ids = [match_id.find("a").get("href").split("/")[2] for match_id in all_matches]
        return match_ids[:num_matches]
    else:
        print("There has been an error, perform manual intervention")
        return


def main_process():
    match_dict = {}
    if properties.match_ids:
        for match in properties.match_ids:
            players_list = []
            match_counter = 0
            match_data = extract_match_data(match)
            html_soup = BeautifulSoup(match_data.content, "html.parser")
            for player_id in properties.player_ids:
                temp_player_dict = {}
                temp_player_dict["player_id"] = player_id
                player_data = html_soup.find("tr", {"class": "player-" + player_id})
                if player_data:
                    match_counter += 1
                    level = player_data.find("span", {"class":"overlay-text"}).get_text()
                    temp_player_dict["max_lvl"] = level
                    # Find the played hero
                    player_hero_container = player_data.find("div", {"class":"image-container-hero"})
                    hero = player_hero_container.find("a").get("href").split("/")[2]
                    temp_player_dict["played_hero"] = hero
                    # Group-1: Kills, Deaths, Assist,Total Gold Earned
                    stats1 = player_data.find_all("td", {"class":"r-group-1"})
                    stats1_data = [stat.get_text() for stat in stats1]
                    temp_player_dict["kills"] = stats1_data[0]
                    temp_player_dict["deaths"] = stats1_data[1]
                    temp_player_dict["assist"] = stats1_data[2]
                    temp_player_dict["net"] = stats1_data[3]
                    # Group-2: Last Hit, Deny, GPM,XPM
                    stats2 = player_data.find_all("td", {"class": "r-group-2"})
                    stats2_data = [stat.get_text() for stat in stats2]
                    temp_player_dict["lh"] = stats2_data[0]
                    temp_player_dict["dn"] = stats2_data[1]
                    temp_player_dict["gpm"] = stats2_data[2]
                    temp_player_dict["xpm"] = stats2_data[3]

                    #Group-3: DMG, HEAL, BLD
                    stats3 = player_data.find_all("td", {"class": "r-group-3"})
                    stats3_data = [stat.get_text() for stat in stats3]
                    temp_player_dict["dmg"] = stats3_data[0]
                    temp_player_dict["heal"] = stats3_data[1]
                    temp_player_dict["bld"] = stats3_data[2]

                    #Group-4: Items
                    stats4 = player_data.find_all("div", {"class": "image-container-item"})
                    player_items = [stat_item.find("a").get('href').split("/")[2] for stat_item in stats4]
                    temp_player_dict["items"] = player_items
                    players_list.append(temp_player_dict)
                else:
                    print("Not a known player for the match...")

            if match_counter >= 3:
                print(" {} People in party ".format(str(match_counter)))
                match_dict[match] = players_list
            # Not to get banned
            time.sleep(2)
        extraction_data["matches"] = match_dict
        return extraction_data
    else:
        return


#print(main_process())

# Main execution
if __name__ == "__main__":
    #print(main_process())
    #Extract player data
    player_infos = player_info()
    # Save it as pickle
    utility.save_data("player_data", player_infos)

#For loading the player infos
#utility.load_data("player_data")

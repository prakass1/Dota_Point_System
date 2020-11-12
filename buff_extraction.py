import requests
from bs4 import BeautifulSoup
import traceback
import properties
import time
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


def main_process():
    match_dict = {}
    for match in properties.match_ids:
        players_list = []
        match_data = extract_match_data(match)
        html_soup = BeautifulSoup(match_data.content, "html.parser")
        for player_id in properties.player_ids:
            temp_player_dict = {}
            temp_player_dict["player_id"] = player_id
            player_data = html_soup.find("tr", {"class": "player-" + player_id})
            if player_data:
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
                print("Not a known player")
        match_dict[match] = players_list
        # Not to get banned
        time.sleep(10)
    extraction_data["matches"] = match_dict
    return extraction_data

# Main execution
#if __name__ == "__main__":
#    print(main_process())

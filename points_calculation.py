import buff_extraction
import pickle
import utility
from jinja2 import Environment, FileSystemLoader
import traceback

#points distribution per player per match
#calculate kill points
def calc_killp(kills):
    return kills * 10

#calculate assist points
def calc_assistp(assist):
    return assist * 5

#calculate death points
def calc_deathsp(deaths):
    return deaths * -2

#calculate last hit points
def calc_lhp(lh):
    if lh < 50:
        lhp = 2
    elif 50 < lh < 100:
        lhp = 3
    elif 100 < lh < 150:
        lhp = 5
    elif 150 < lh < 200:
        lhp = 7
    elif 200 < lh:
        lhp = 10
    else:
        lhp = 10
    return lhp

#calculate deny points
def calc_dnp(dn):
    if 1 < dn < 5:
        dnp = 2
    elif 5 < dn < 10:
        dnp = 5
    elif 10 < dn < 15:
        dnp = 7
    elif dn > 15:
        dnp = 10
    return dnp

#calculate gold per minute points
def calc_gpmp(gpm):
    if gpm < 500:
        gpmp = 2
    elif 500 < gpm < 1000:
        gpmp = 3
    elif 1000 < gpm < 1500:
        gpmp = 5
    elif 1500 < gpm < 2000:
        gpmp = 7
    elif 2000 < gpm:
        gpmp = 10
    else:
        gpmp = 10
    return gpmp

#calculate xp per minute points
def calc_xpmp(xpm):
    if xpm < 500:
        xpmp = 2
    elif 500 < xpm < 1000:
        xpmp = 3
    elif 1000 < xpm < 1500:
        xpmp = 5
    elif 1500 < xpm < 2000:
        xpmp = 7
    elif 2000 < xpm:
        xpmp = 10
    else:
        xpmp = 10
    return xpmp

#calculate damage points
def calc_dmgp(dmg):
    if dmg > 100000:
        dmgp = 10
    else:
        dmgp = 0
    return dmgp

#calculate building damage points
def calc_bldp(bld):
    if bld < 2000:
        bldp = 2
    elif 2000 < bld < 5000:
        bldp = 3
    elif 5000 < bld < 10000:
        bldp = 5
    elif 10000 < bld < 15000:
        bldp = 7
    elif 15000 < bld:
        bldp = 10
    else:
        bldp = 10
    return bldp

#calculate heal points
def calc_healp(heal):
    if heal < 2000:
        healp = 2
    elif 2000 < heal < 5000:
        healp = 3
    elif 5000 < heal < 10000:
        healp = 5
    elif 10000 < heal < 15000:
        healp = 7
    elif 15000 < heal:
        healp = 10
    elif heal == "-":
        healp = 0
    else:
        healp = 10
    return healp

#calculate level points if lvl = 30
def calc_lvlp(lvl):
    if lvl == 30:
        lvlp = 10
    else:
        lvlp = 0
    return lvlp

#calculate item points
def calc_itemp(item):
    itemp = 0
    for each in item:
        if each == 'magic-wand':
            itemp += 5
        elif each == 'tranquil-boots':
            itemp += 10
        elif each == 'arcane-boots':
            itemp += 15
        elif each == 'aether-lens':
            itemp += 10
        elif each == 'force-staff':
            itemp += 15
        elif each == 'glimmer-cape':
            itemp += 15
        elif each == 'smoke-of-deceit':
            itemp += 5
        elif each == 'sentry-ward':
            itemp += 10
        elif each == 'ghost-scepter':
            itemp += 10
        elif each == 'observer-ward':
            itemp += 10
        elif each == 'assault-cuirass':
            itemp += 15
        elif each == 'spirit-vessel':
            itemp += 15
        elif each == 'heavens-halberd':
            itemp += 10
        elif each == 'lotus-orb':
            itemp += 20
        elif each == 'urn-of-shadows':
            itemp += 10
        elif each == 'aeon-disk':
            itemp += 15
        elif each == 'vladimirs-offering':
            itemp += 15
        elif each == 'hood-of-defiance':
            itemp += 10
        elif each == 'mekansm':
            itemp += 15
        elif each == 'gem-of-true-sight':
            itemp += 15
        elif each == 'solar-crest':
            itemp += 15
        elif each == 'medallion-of-courage':
            itemp += 10
        elif each == 'observer-and-sentry-wards':
            itemp += 15
        elif each == 'dust-of-appearance':
            itemp += 10
        elif each == 'guardian-greaves':
            itemp += 20
        elif each == 'crimson-guard':
            itemp += 20
        elif each == 'pipe-of-insight':
            itemp += 20
        else:
            itemp += 0
    return itemp


def calculate_points(extraction_data):
    # total points
    total_points_data = {}
    for match, player in extraction_data['matches'].items():
        for stat in player:
            #kill
            if stat['kills'] == "-":
                Kill_Points = 0
            else:
                k = int(stat['kills'])
                Kill_Points = calc_killp(k)

            #death
            if stat['deaths'] == "-":
                Death_Points = 0
            else:
                d = int(stat['deaths'])
                Death_Points = calc_deathsp(d)

            #assist
            if stat['assist'] == "-":
                Assist_Points = 0
            else:
                a = int(stat['assist'])
                Assist_Points = calc_assistp(a)

            #last hit
            #assist
            if stat['lh'] == "-":
                Last_Hit_Points = 0
            else:
                lh = int(stat['lh'])
                Last_Hit_Points = calc_lhp(lh)

            #denies
            if stat['dn'] == "":
                Deny_Points = 0
            else:
                dn = int(stat['dn'])
                Deny_Points = calc_dnp(dn)

            #gold per minute
            if stat["gpm"] == "-":
                Gold_Per_Minute_Points = 0
            else:
                gpm = int(stat['gpm'])
                Gold_Per_Minute_Points = calc_gpmp(gpm)

            #building damage
            if "k" in stat["bld"]:
                bld = float(stat["bld"].split("k")[0]) * 1000
                Building_Damage_Points = calc_bldp(bld)
            elif stat["bld"] == "-":
                Building_Damage_Points = 0
            else:
                bld = float(stat["bld"])
                Building_Damage_Points = calc_bldp(bld)

            #xp per minute
            if "k" in stat["xpm"]:
                xpm = float(stat["xpm"].split("k")[0]) * 1000
                Experience_Per_Minute_Points = calc_xpmp(xpm)
            else:
                xpm = float(stat["xpm"])
                Experience_Per_Minute_Points = calc_xpmp(xpm)

            #damage > 100k gets bonus
            if "k" in stat["dmg"]:
                dmg = float(stat["dmg"].split("k")[0]) * 1000
                Damage_Points = calc_dmgp(dmg)
            elif stat["dmg"] == "-":
                Damage_Points = 0
            else:
                dmg = float(stat["dmg"])
                Damage_Points = calc_dmgp(dmg)

            #heal points (some values in heal are '-')
            if stat['heal'] == "-":
                Heal_Points = 0
            elif "k" in stat["heal"]:
                heal = float(stat["heal"].split("k")[0]) * 1000
                Heal_Points = calc_healp(heal)
            else:
                Heal_Points = int(stat['heal'])
                Heal_Points = calc_healp(heal)

            #level points if max level of 30 reached
            lvl = int(stat['max_lvl'])
            Max_Level_Points = calc_lvlp(lvl)

            #item points (support items inflated)
            player_item = stat['items']
            Item_Points = calc_itemp(player_item)

            total_Points = Kill_Points + Death_Points + Assist_Points + Last_Hit_Points + Deny_Points \
                        + Gold_Per_Minute_Points + Experience_Per_Minute_Points \
                        + Damage_Points + Building_Damage_Points \
                        + Heal_Points + Max_Level_Points + Item_Points

            temp_data_store = {"player_id": stat["player_id"],
                               "score": total_Points,
                               "games_played": 1,
                               "player_rating": 0}

            # Load the player info into the temp_data_store
            player_data = utility.load_data("player_data")
            if player_data:
                if stat["player_id"] in player_data:
                    temp_data_store["player_name"] = player_data[stat["player_id"]]["name"]
                    temp_data_store["img_url"] = player_data[stat["player_id"]]["image_url"]
            else:
                temp_data_store["player_name"] = player_data[stat["player_id"]]
                temp_data_store["img_url"] = ""

            if stat["player_id"] not in total_points_data:
                total_points_data[stat["player_id"]] = temp_data_store
            else:
                temp_data_store = total_points_data[stat["player_id"]]
                temp_data_store["score"] = temp_data_store["score"] + total_points
                temp_data_store["games_played"] += 1
                temp_data_store["player_rating"] = temp_data_store["score"] / temp_data_store["games_played"]
                total_points_data[stat["player_id"]] = temp_data_store

            #print("For Match id " + match + " player id is " + stat['player_id'] + " and Total Points = " + str(Total_Points))

    # Sort in descending order of points and add each of the player into the ranked list.
    player_scores = [infos["score"] for infos in total_points_data.values()]
    player_scores.sort(reverse=True)
    ranked_list = []
    for score in player_scores:
        for k, v in total_points_data.items():
            if score == v["score"]:
                ranked_list.append(v)

    return ranked_list


def write_template(total_points):
    try:
        file_loader = FileSystemLoader("templates")
        env = Environment(loader=file_loader)
        template = env.get_template("table.html")
        output = template.render(ranked_list=total_points)
        f_op = open("docs/index.html", "w", encoding="utf-8")
        f_op.write(output)
        f_op.close()
    except IOError:
        print("Error while writing")
        traceback.print_exc()
        f_op.close()

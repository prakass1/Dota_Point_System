import buff_extraction
import pickle
# Get the data from dotabuff first
extraction_data = buff_extraction.main_process()

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
for match, player in extraction_data['matches'].items():
    for stat in player:
        #kill
        k = int(stat['kills'])
        kp = calc_killp(k)

        #death
        d = int(stat['deaths'])
        dp = calc_deathsp(d)

        #assist
        a = int(stat['assist'])
        ap = calc_assistp(a)

        #last hit
        lh = int(stat['lh'])
        lhp = calc_lhp(lh)
        
        #denies
        if stat['dn'] == "":
            dnp = 0
        else:
            dn = int(stat['dn'])
            dnp = calc_dnp(dn)

        #gold per minute
        gpm = int(stat['gpm'])
        gpmp = calc_gpmp(gpm)

        #building damage
        if "k" in stat["bld"]:
            bld = float(stat["bld"].split("k")[0]) * 1000
            bldp = calc_bldp(bld)
        else:
            bld = float(stat["bld"])
            bldp = calc_bldp(bld)

        #xp per minute
        if "k" in stat["xpm"]:
            xpm = float(stat["xpm"].split("k")[0]) * 1000
            xpmp = calc_xpmp(xpm)
        else:
            xpm = float(stat["xpm"])
            xpmp = calc_xpmp(xpm)

        #damage > 100k gets bonus
        if "k" in stat["dmg"]:
            dmg = float(stat["dmg"].split("k")[0]) * 1000
            dmgp = calc_dmgp(dmg)
        else:
            dmg = float(stat["dmg"])
            dmgp = calc_dmgp(dmg)

        #heal points (some values in heal are '-')
        if stat['heal'] == "-":
            healp = 0
        else:
            heal = int(stat['heal'])
            healp = calc_healp(heal)
        
        #level points if max level of 30 reached
        lvl = int(stat['max_lvl'])
        lvlp = calc_lvlp(lvl)
        
        Total_Points = kp + dp + ap + lhp + gpmp + healp + bldp + lvlp + dnp + xpmp + dmgp

        print("For Match id " + match + " player id is " + stat['player_id'] + " and Total Points = " + str(Total_Points))
        
# # To add is a final data store as follows:
# total_points = {
#     "p1": {
#         "score": val,
#         "games_played": val
#     },
#     "p2": {
#         "score": val,
#         "games_played": val
#     }
# }

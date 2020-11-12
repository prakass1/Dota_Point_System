import buff_extraction

#points distribution
def calc_killp(kills):
    return kills * 10

def calc_assistp(assist):
    return assist * 5

def calc_deathsp(deaths):
    return deaths * -2

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

for match, player in buff_extraction.extraction_data['matches'].items():
    for stat in player:
        k = int(stat['kills'])
        kp = calc_killp(k)
        d = int(stat['deaths'])
        dp = calc_deathsp(d)
        a = int(stat['assist'])
        ap = calc_assistp(a)
        lh = int(stat['lh'])
        lhp = calc_lhp(lh)
        gpm = int(stat['gpm'])
        gpmp = calc_gpmp(gpm)
        #bld = int(float(stat['bld']))
        #bldp = calc_bldp(bld)
        if stat['heal'] == "-":
            healp = 0
        else:
            heal = int(stat['heal'])
            healp = calc_healp(heal)
        
        Total_Points = kp + dp + ap + lhp + gpmp + bldp + healp

        print("player id is " + stat['player_id'] + " and Total Points =" + str(Total_Points))
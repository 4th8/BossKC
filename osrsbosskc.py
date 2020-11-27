import requests
import csv

username = input("Enter a username:")
username = username.replace(' ','%20')
uri = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=' + username
response = requests.get(uri)

def parseresponse(response):
    user = {'skills': {}, 'Bosses': {}, 'clues': {},}
    lines = response.text.split('\n')

    skills = ['Overall', 'Attack', 'Defence', 'Strength', 'Hitpoints', 'Ranged', 'Prayer', 'Magic', 'Cooking', 'Woodcutting', 'Fletching', 'Fishing', 'Firemaking', 'Crafting', 'Smithing', 'Mining', 'Herblore', 'Agility', 'Thieving', 'Slayer', 'Farming', 'Runecrafting', 'Hunter', 'Construction']
    for s in skills:
        curentline = lines[skills.index(s)].split(',')
        overall = {}
        overall['rank'] = curentline[0]
        overall['level'] = curentline[1]
        overall['xp'] = curentline[2]
        user['skills'][s] = overall

    clueTypes = ['All','beginner','easy', 'medium', 'hard','elite','master']
    for type in clueTypes:
        curentline = lines[(clueTypes.index(type)+26)].split(',')
        overall = {}
        overall['rank'] = curentline[0]
        overall['kc'] = curentline[1]
        user['clues'][type] = overall

    bossNames = ['Abyssal Sire','Alchemical Hydra','Barrows Chests','Bryophyta','Callisto','Cerberus','Chambers of Xeric','Chambers of Xeric: Challenge Mode','Chaos Elemental','Chaos Fanatic','Commander Zilyana','Corporeal Beast','Crazy Archaeologist','Dagannoth Prime','Dagannoth Rex','Dagannoth Supreme','Deranged Archaeologist','General Graardor','Giant Mole','Grotesque Guardians','Hespori','Kalphite Queen','King Black Dragon','Kraken','KreeArra','Kril Tsutsaroth','Mimic','Nightmare','Obor','Sarachnis','Scorpia','Skotizo','The Gauntlet','The Corrupted Gauntlet','Theatre of Blood','Thermonuclear Smoke Devil','TzKal-Zuk','TzTok-Jad','Venenatis','Vetion','Vorkath','Wintertodt','Zalcano','Zulrah']
    for boss in bossNames:
        curentline = lines[(bossNames.index(boss)+35)].split(',')
        overall = {}
        overall['name'] = boss
        overall['rank'] = int(curentline[0])
        overall['kc'] = int(curentline[1])
        user['Bosses'][boss] = overall
    return user

def gettotalbosskc(user):
    total = 0
    for boss in user['Bosses'].keys():
        if (user['Bosses'][boss]['name'] == 'Chambers of Xeric: Challenge Mode' or user['Bosses'][boss]['name'] == 'Theatre of Blood'):
            total = total + (user['Bosses'][boss]['kc'] * 4)
        elif (user['Bosses'][boss]['name'] == 'Chambers of Xeric'):
            total = total + (user['Bosses'][boss]['kc'] * 2)
        else:
             total = total + user['Bosses'][boss]['kc']

    return total

if(response):
    user = parseresponse(response)
    print('Total boss kc: ' + str(gettotalbosskc(user)))
    print('Total Level: ' + str(user['skills']['Overall']['level']))
else:
    print('username not found')
import requests


# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = 'cce3079463cb1a977cc70b6033d553de'

SPORT = 'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'eu' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# First get a list of in-season sports
#   The sport 'key' from the response can be used to get odds in the next request
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

sports_response = requests.get(
    'https://api.the-odds-api.com/v4/sports', 
    params={
        'api_key': API_KEY
    }
)


if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

else:
    print('List of in season sports:', sports_response.json())


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()
    print('Number of events:', len(odds_json))
    ODD_DATA = []
    for event in odds_json:
        HOME_NAME = event["home_team"]
        AWAY_NAME = event["away_team"]
        OOD_1 = 0
        OOD_2 = 0
        ODD_DRAW = 0
        bookmaker_index = [0,0,0]
        DRAW=False
        for index,bookmaker in enumerate(event["bookmakers"]):
            odds_list = bookmaker["markets"][0]["outcomes"]
            if OOD_1 < odds_list[0]["price"]:
                OOD_1 = odds_list[0]["price"]
                bookmaker_index[0] = index
            if OOD_2 < odds_list[1]["price"]:
                OOD_2 = odds_list[1]["price"]
                bookmaker_index[1] = index
            if len(odds_list) > 2:
                DRAW = True
                if ODD_DRAW < odds_list[2]["price"]:
                    ODD_DRAW = odds_list[2]["price"]
                    bookmaker_index[2] = index
        if DRAW:
            export_list = [HOME_NAME,AWAY_NAME,OOD_1,OOD_2,ODD_DRAW,bookmaker_index]
        else:
            export_list = [HOME_NAME,AWAY_NAME,OOD_1,OOD_2,bookmaker_index]
        ODD_DATA.append(export_list)
    print(ODD_DATA)
    for index,event in enumerate(odds_json):
        if len(ODD_DATA[index]) < 4:
            result = "{} = {}\n {} = {}\n {} vs {}\n".format(event["bookmakers"][ODD_DATA[index][-1][0]]['title'],ODD_DATA[index][2],event["bookmakers"][ODD_DATA[index][-1][1]]['title'],ODD_DATA[index][3],ODD_DATA[index][0],ODD_DATA[index][1])
        else:
            result = "{} = {}\n {} = {}\n Draw {} = {}\n {} vs {}\n".format(event["bookmakers"][ODD_DATA[index][-1][0]]['title'],ODD_DATA[index][2],event["bookmakers"][ODD_DATA[index][-1][1]]['title'],ODD_DATA[index][3],event["bookmakers"][ODD_DATA[index][-1][2]]['title'],ODD_DATA[index][4],ODD_DATA[index][0],ODD_DATA[index][1])
        print(result)
                
            
                        


    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])

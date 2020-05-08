import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import json


TeamLookup = {
    'ARI': 'Cardinals',
    'CRD': 'Cardinals',
    'ATL': 'Falcons',
    'BAL': 'Ravens',
    'RAV': 'Ravens',
    'BUF': 'Bills',
    'CAR': 'Panthers',
    'CHI': 'Bears',
    'CIN': 'Bengals',
    'CLE': 'Browns',
    'DAL': 'Cowboys',
    'DEN': 'Broncos',
    'DET': 'Lions',
    'GNB': 'Packers',
    'HOU': 'Texans',
    'IND': 'Colts',
    'CLT': 'Colts',
    'JAC': 'Jaguars',
    'JAX': 'Jaguars',
    'KC': 'Chiefs',
    'KAN': 'Chiefs',
    'SDG': 'Chargers',
    'LAC': 'Chargers',
    'LAR': 'Rams',
    'RAM': 'Rams',
    'MIA': 'Dolphins',
    'MIN': 'Vikings',
    'NE': 'Patriots',
    'NO': 'Saints',
    'NWE': 'Patriots',
    'NOR': 'Saints',
    'NYG': 'Giants',
    'NYJ': 'Jets',
    'OAK': 'Raiders',
    'RAI': 'Raiders',
    'PHI': 'Eagles',
    'PIT': 'Steelers',
    'SF': '49ers',
    'SFO': '49ers',
    'SEA': 'Seahawks',
    'TB': 'Buccaneers',
    'TAM': 'Buccaneers',
    'TEN': 'Titans',
    'WAS': 'Redskins',
    'OTI': 'Titans'
}





def get_gameplays():

    PlayTypeDict = {}

    PlayTypeStrings = {
        'Pass': ['pass incomplete', 'pass complete', 'sacked'],
        'Admin': ['Timeout', 'Penalty', 'aborted'],
        'Kneel': ['knee', 'knelt'],
        'Special Teams': ['kicks off', 'punts', 'field goal', 'spiked the ball', 'kicks onside', 'no good'],
        'Run': ['left end','right end', ' for ', 'up the middle', 'middle for', 'left tackle','left guard','right guard', 'right tackle'],
    }

    for Year in range(1999, 2001):

        PlayTypeCounts = {
            'Pass': 0,
            'Run': 0,
            'Admin': 0,
            'Kneel': 0,
            'Special Teams': 0
        }
        for GameNumber in range(1,17):
            PlayTypeDict = {}
            print('Game', GameNumber, 'in', Year)
            for Period in [ '1', '2', '3','4']:
                if Period not in PlayTypeDict:
                    PlayTypeDict[Period] = {}
                for Down in ['1', '2', '3', '4']:
                    path = 'https://widgets.sports-reference.com/wg.fcgi?css=1&site=pfr&url=%2Fplay-index%2Fplay_finder.cgi%3Frequest%3D1%26match%3Dall%26year_min%3D{YEAR}%26year_max%3D{YEAR}%26game_type%3DR%26game_num_min%3D{GameNumber}%26game_num_max%3D{GameNumber}%26week_num_min%3D0%26week_num_max%3D99%26game_location%3DH%26quarter%255B%255D%3D{Period}%26minutes_max%3D15%26seconds_max%3D0%26minutes_min%3D0%26seconds_min%3D0%26down%255B%255D%3D{Down}%26field_pos_min_field%3Dteam%26field_pos_max_field%3Dteam%26end_field_pos_min_field%3Dteam%26end_field_pos_max_field%3Dteam%26type%255B%255D%3DPASS%26type%255B%255D%3DRUSH%26type%255B%255D%3DPUNT%26type%255B%255D%3DKOFF%26type%255B%255D%3DONSD%26type%255B%255D%3DFG%26type%255B%255D%3DXP%26type%255B%255D%3D2PC%26no_play%3DN%26turnover_type%255B%255D%3Dinterception%26turnover_type%255B%255D%3Dfumble%26score_type%255B%255D%3Dtouchdown%26score_type%255B%255D%3Dfield_goal%26score_type%255B%255D%3Dsafety%26order_by%3Dyds_to_go&div=div_all_plays&del_col=1,11,12,13,14'.format(Period=Period, Down=Down, YEAR=Year, GameNumber = GameNumber)

                    if Down not in PlayTypeDict[Period]:
                        PlayTypeDict[Period][Down] = {}

                    req = get(path)

                    if req.status_code==200 :
                        soup = BeautifulSoup(req.content, 'html.parser')
                        table = soup.find('table')
                        if table is not None:
                            df = pd.read_html(str(table))[0]
                            df.columns = ['OffenseTeam', 'DefenseTeam', 'Period', 'TimeRemaining', 'Down', 'YardsToGo', 'BallSpot', 'Score', 'Event']



                            data = df.to_dict('records')
                            cleansed_data = []
                            TeamList = []
                            for Play in data:
                                BallSpotSplit = Play['BallSpot'].split(' ')
                                if len(BallSpotSplit) == 2:
                                    Play['PlayType'] = None
                                    Play['BallSpotTeam'] = BallSpotSplit[0]
                                    if Play['BallSpotTeam'] not in TeamList:
                                        TeamList.append(Play['BallSpotTeam'])

                                    Play['BallSpotTeam'] = TeamLookup[Play['BallSpotTeam'] ]
                                    Play['BallSpotYard'] = int(BallSpotSplit[1])


                                    if Play['BallSpotYard'] is None:
                                        Play['BallSpotYard'] = 0

                                    if Play['BallSpotTeam'] == Play['OffenseTeam']:
                                        Play['BallSpotYard'] = Play['BallSpotYard']
                                    elif Play['BallSpotTeam'] == Play['DefenseTeam']:
                                        Play['BallSpotYard'] = 100 - Play['BallSpotYard']
                                    else :
                                        print('Couldnt match ', Play['BallSpotTeam'], Play['OffenseTeam'], Play['DefenseTeam'])
                                        Play['BallSpotYard'] = -100




                                    ScoreSplit = Play['Score'].split('-')
                                    Play['Lead'] = int(ScoreSplit[0]) - int(ScoreSplit[1])



                                    Play['YardsToGoClass'] = ''
                                    #YardsToGoClass
                                    if Play['YardsToGo'] >= 1 and Play['YardsToGo'] <= 2:
                                        Play['YardsToGoClass'] = '1-2'
                                    if Play['YardsToGo'] >= 3 and Play['YardsToGo'] <= 5:
                                        Play['YardsToGoClass'] = '3-5'
                                    if Play['YardsToGo'] >= 6 and Play['YardsToGo'] <= 10:
                                        Play['YardsToGoClass'] = '6-10'
                                    if Play['YardsToGo'] >= 11:
                                        Play['YardsToGoClass'] = '11-100'

                                    if Play['YardsToGoClass'] not in PlayTypeDict[Period][Down]:
                                        PlayTypeDict[Period][Down][Play['YardsToGoClass']] = {}

                                    #BallSpotClass
                                    Play['BallSpotClass'] = ''



                                    if Play['BallSpotClass'] not in PlayTypeDict[Period][Down][Play['YardsToGoClass']]:
                                        PlayTypeDict[Period][Down][Play['YardsToGoClass']][Play['BallSpotClass']] = {}


                                    Play['LeadClass'] = ''
                                    #LeadClass


                                    if Play['LeadClass'] not in PlayTypeDict[Period][Down][Play['YardsToGoClass']][Play['BallSpotClass']]:
                                        PlayTypeDict[Period][Down][Play['YardsToGoClass']][Play['BallSpotClass']][Play['LeadClass']] = PlayTypeCounts.copy()


                                    PlayTypeFound = False
                                    for PlayType in PlayTypeStrings:
                                        for EventString in PlayTypeStrings[PlayType]:
                                            if EventString.lower() in Play['Event'].lower() and not PlayTypeFound:
                                                Play['PlayType'] = PlayType
                                                PlayTypeFound = True
                                                PlayTypeDict[Period][Down][Play['YardsToGoClass']][Play['BallSpotClass']][Play['LeadClass']] [Play['PlayType']] += 1


                                    if PlayTypeFound == False:
                                        print('Couldnt find', Play['Event'])


                                    cleansed_data.append(Play)

                        else:
                            print('None table: ', Down, 'Down', Period, 'Period', GameNumber, 'GameNumber', Year, 'Year')

            with open('PlayTypeCounts-Year-'+str(Year)+'-Game-'+str(GameNumber)+'.json', 'w') as outfile:
                json.dump(PlayTypeDict, outfile)

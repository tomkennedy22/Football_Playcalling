import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import json


TeamLookup = {
    'CRD': 'Cardinals',
    'ATL': 'Falcons',
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
    'CLT': 'Colts',
    'JAX': 'Jaguars',
    'HTX': 'Texans',
    'KAN': 'Chiefs',
    'SDG': 'Chargers',
    'RAM': 'Rams',
    'MIA': 'Dolphins',
    'MIN': 'Vikings',
    'NWE': 'Patriots',
    'NOR': 'Saints',
    'NYG': 'Giants',
    'NYJ': 'Jets',
    'RAI': 'Raiders',
    'PHI': 'Eagles',
    'PIT': 'Steelers',
    'SFO': '49ers',
    'SEA': 'Seahawks',
    'TAM': 'Buccaneers',
    'WAS': 'Redskins',
    'OTI': 'Titans'
}


class Lead:

    def __init__(self, Floor = 0, Ceiling = 0):
        self.Floor = Floor
        self.Ceiling = Ceiling

    def __str__(self):
        s = 'Lead:'
        if self.Floor < 0:
            s+= '!'
        s+=str(abs(self.Floor))

        s += '-'
        if self.Ceiling < 0:
            s+= '!'
        s+=str(abs(self.Ceiling))

        return s

    def __repr__(self):
        return str(self)


class BallSpot:

    def __init__(self, Floor = 0, Ceiling = 0):
        self.Floor = Floor
        self.Ceiling = Ceiling

    def __str__(self):
        s = 'BallSpot:'
        if self.Floor < 0:
            s+= '!'
        s+=str(abs(self.Floor))

        s += '-'
        if self.Ceiling < 0:
            s+= '!'
        s+=str(abs(self.Ceiling))

        return s

    def __repr__(self):
        return str(self)

class YardsToGo:

    def __init__(self, Floor = 0, Ceiling = 0):
        self.Floor = Floor
        self.Ceiling = Ceiling

    def __str__(self):
        s = 'YardsToGo:'
        if self.Floor < 0:
            s+= '!'
        s+=str(abs(self.Floor))

        s += '-'
        if self.Ceiling < 0:
            s+= '!'
        s+=str(abs(self.Ceiling))

        return s

class TimeLeft:

    def __init__(self, HalfEnd = False, GameEnd = False, Floor = 0, Ceiling = 0):
        self.HalfEnd = HalfEnd
        self.GameEnd = GameEnd
        self.Floor = Floor
        self.Ceiling = Ceiling

    def __str__(self):
        s = 'TimeLeft:'
        if self.Floor < 0:
            s+= '!'
        s+=str(abs(self.Floor))

        s += '-'
        if self.Ceiling < 0:
            s+= '!'
        s+=str(abs(self.Ceiling))

        if self.GameEnd:
            s+=':GameEnd'
        elif self.HalfEnd:
            s+=':HalfEnd'

        return s

    def __repr__(self):
        return str(self)

def MatchFloorCeiling(Val, Objs):
    Val = int(Val)
    for ObjStr, Obj in Objs.items():
        if Val >= Obj.Floor and Val <= Obj.Ceiling:
            return Obj


def MatchFloorCeilingTime(Val, Objs, HalfEnd, GameEnd):
    Val = int(Val)
    for ObjStr, Obj in Objs.items():
        if Val >= Obj.Floor and Val <= Obj.Ceiling and Obj.HalfEnd == HalfEnd and GameEnd == Obj.GameEnd:
            return Obj

def MinutesToSeconds(Val):

    if ':' in Val:
        TimeSplit = Val.split(':')
        Minutes = int(TimeSplit[0])
        Seconds = int(TimeSplit[1])

        return Minutes * 60 + Seconds
    else:
        print('Abnormal time:', Val)
        return int(Val)

def isNaN(Val):
    return Val != Val

LeadInits = [{'Floor': -100, 'Ceiling': -17}
           , {'Floor': -16, 'Ceiling': -14}
           , {'Floor': -13, 'Ceiling': -9}
           , {'Floor': -8, 'Ceiling': -7}
           , {'Floor': -6, 'Ceiling': -5}
           , {'Floor': -4, 'Ceiling': -3}
           , {'Floor': -2, 'Ceiling': -1}
           , {'Floor': 0, 'Ceiling': 0}
           , {'Floor': 1, 'Ceiling': 2}
           , {'Floor': 3, 'Ceiling': 4}
           , {'Floor': 5, 'Ceiling': 6}
           , {'Floor': 7, 'Ceiling': 8}
           , {'Floor': 9, 'Ceiling': 13}
           , {'Floor': 14, 'Ceiling': 16}
           , {'Floor': 17, 'Ceiling': 100}]

Leads = {str(L): L for L in [Lead(**LeadVals) for LeadVals in LeadInits]}

BallSpotInits = [{'Floor': 1, 'Ceiling': 10}
                ,{'Floor': 11, 'Ceiling': 20}
                ,{'Floor': 21, 'Ceiling': 30}
                ,{'Floor': 31, 'Ceiling': 40}
                ,{'Floor': 41, 'Ceiling': 50}
                ,{'Floor': 51, 'Ceiling': 55}
                ,{'Floor': 56, 'Ceiling': 60}
                ,{'Floor': 61, 'Ceiling': 65}
                ,{'Floor': 66, 'Ceiling': 70}
                ,{'Floor': 71, 'Ceiling': 75}
                ,{'Floor': 76, 'Ceiling': 80}
                ,{'Floor': 81, 'Ceiling': 85}
                ,{'Floor': 86, 'Ceiling': 90}
                ,{'Floor': 91, 'Ceiling': 100}]

BallSpots = {str(BS): BS for BS in [BallSpot(**BallSpotVals) for BallSpotVals in BallSpotInits]}


YardsToGoInits = [{'Floor': 1, 'Ceiling': 10}
                ,{'Floor': 11, 'Ceiling': 20}
                ,{'Floor': 21, 'Ceiling': 30}
                ,{'Floor': 31, 'Ceiling': 40}
                ,{'Floor': 41, 'Ceiling': 50}
                ,{'Floor': 51, 'Ceiling': 55}
                ,{'Floor': 56, 'Ceiling': 60}
                ,{'Floor': 61, 'Ceiling': 65}
                ,{'Floor': 66, 'Ceiling': 70}
                ,{'Floor': 71, 'Ceiling': 75}
                ,{'Floor': 76, 'Ceiling': 80}
                ,{'Floor': 81, 'Ceiling': 85}
                ,{'Floor': 86, 'Ceiling': 90}
                ,{'Floor': 91, 'Ceiling': 100}]

YardsToGos = {str(YTG): YTG for YTG in [YardsToGo(**YardsToGoVals) for YardsToGoVals in YardsToGoInits]}


TimeLeftInits = [
    {'Floor': 0, 'Ceiling': 900, 'GameEnd': False, 'HalfEnd': False},
    {'Floor': 0, 'Ceiling': 20, 'GameEnd': False, 'HalfEnd': True},
    {'Floor': 21, 'Ceiling': 60, 'GameEnd': False, 'HalfEnd': True},
    {'Floor': 61, 'Ceiling': 180, 'GameEnd': False, 'HalfEnd': True},
    {'Floor': 181, 'Ceiling': 300, 'GameEnd': False, 'HalfEnd': True},
    {'Floor': 0, 'Ceiling': 20, 'GameEnd': True, 'HalfEnd': True},
    {'Floor': 21, 'Ceiling': 60, 'GameEnd': True, 'HalfEnd': True},
    {'Floor': 61, 'Ceiling': 180, 'GameEnd': True, 'HalfEnd': True},
    {'Floor': 181, 'Ceiling': 300, 'GameEnd': True, 'HalfEnd': True},
    {'Floor': 301, 'Ceiling': 600, 'GameEnd': True, 'HalfEnd': True},
]

TimeLefts = {str(TL): TL for TL in [TimeLeft(**TimeLeftVals) for TimeLeftVals in TimeLeftInits]}






def get_gameplays():

    PlayTypeDict = {}

    PlayTypeStrings = {
        'Pass': ['pass incomplete', 'pass complete', 'sacked'],
        'Admin': ['spiked the ball','Timeout', 'Penalty', 'aborted'],
        'Kneel': ['knee', 'knelt'],
        'Punt': ['Punts'],
        'Field Goal': ['field goal','no good'],
        'Special Teams': ['kicks off',  'kicks onside', 'extra point', 'two point'],
        'Run': ['left end','right end', ' for ', 'up the middle', 'middle for', 'left tackle','left guard','right guard', 'right tackle'],
    }

    YearStart = 1998
    YearsToGo = 20
    for Year in range(YearStart, YearStart +YearsToGo):

        PlayTypeCounts = {
            'Pass': 0,
            'Run': 0,
            'Punt': 0,
            'Field Goal': 0,
            'Admin': 0,
            'Kneel': 0,
            'Special Teams': 0
        }
        for GameNumber in range(1,17):
            PlayTypeDict = {}
            for Team in TeamLookup:
                print('Game', GameNumber, 'in', Year, 'for', TeamLookup[Team])
                for GameLocation in ['H', 'A']:
                    path = 'https://widgets.sports-reference.com/wg.fcgi?css=1&site=pfr&url=%2Fplay-index%2Fplay_finder.cgi%3Frequest%3D1%26match%3Dall%26year_min%3D{YEAR}%26year_max%3D{YEAR}%26game_type%3DR%26game_num_min%3D{GameNumber}%26game_num_max%3D{GameNumber}%26week_num_min%3D0%26week_num_max%3D99%26game_location%3D{GameLocation}%26minutes_max%3D15%26seconds_max%3D0%26minutes_min%3D0%26seconds_min%3D0%26team_id%3D{TEAM}%26field_pos_min_field%3Dteam%26field_pos_max_field%3Dteam%26end_field_pos_min_field%3Dteam%26end_field_pos_max_field%3Dteam%26type%255B%255D%3DPASS%26type%255B%255D%3DRUSH%26type%255B%255D%3DPUNT%26type%255B%255D%3DKOFF%26type%255B%255D%3DONSD%26type%255B%255D%3DFG%26type%255B%255D%3DXP%26type%255B%255D%3D2PC%26no_play%3DN%26turnover_type%255B%255D%3Dinterception%26turnover_type%255B%255D%3Dfumble%26score_type%255B%255D%3Dtouchdown%26score_type%255B%255D%3Dfield_goal%26score_type%255B%255D%3Dsafety%26order_by%3Dyds_to_go&div=div_all_plays&del_col=1,11,12,13,14'.format(YEAR=Year, GameNumber = GameNumber, TEAM=Team, GameLocation=GameLocation)
                    req = get(path)
                    try:
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

                                        if isNaN(Play['Period']) or isNaN(Play['Down']):
                                            continue
                                        Play['Period'] = int(Play['Period'])
                                        Play['Down'] = int(Play['Down'])

                                        HalfEnd = True if Play['Period'] in [2,4] else False
                                        GameEnd = True if Play['Period'] == 4 else False

                                        if Play['Period'] not in PlayTypeDict:
                                            PlayTypeDict[Play['Period']] = {}
                                        if Play['Down'] not in PlayTypeDict[Play['Period']]:
                                            PlayTypeDict[Play['Period']][Play['Down']] = {}
                                        Play['PlayType'] = None
                                        Play['BallSpotTeam'] = BallSpotSplit[0]
                                        if Play['BallSpotTeam'] not in TeamList:
                                            TeamList.append(Play['BallSpotTeam'])

                                        Play['BallSpotTeam'] = TeamLookup[Play['BallSpotTeam'] ]
                                        Play['BallSpotYard'] = int(BallSpotSplit[1])

                                        Play['SecondsLeft'] = MinutesToSeconds(Play['TimeRemaining'])

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
                                        if len(ScoreSplit[0]) == 0 or len(ScoreSplit[1]) == 0:
                                            continue
                                        Play['Lead'] = int(ScoreSplit[0]) - int(ScoreSplit[1])
                                        Play['Lead'] = -1 * Play['Lead'] if GameLocation == 'A' else Play['Lead']

                                        #BallSpotClass
                                        Play['BallSpotClass'] = str(MatchFloorCeiling(Play['BallSpotYard'], BallSpots))
                                        Play['YardsToGoClass'] = str(MatchFloorCeiling(Play['YardsToGo'], YardsToGos))
                                        Play['LeadClass'] = str(MatchFloorCeiling(Play['Lead'], Leads))
                                        Play['TimeLeftClass'] = str(MatchFloorCeilingTime(Play['SecondsLeft'], TimeLefts, GameEnd=GameEnd, HalfEnd=HalfEnd))



                                        if Play['YardsToGoClass'] not in PlayTypeDict[Play['Period']][Play['Down']]:
                                            PlayTypeDict[Play['Period']][Play['Down']][Play['YardsToGoClass']] = {}
                                        if Play['BallSpotClass'] not in PlayTypeDict[Play['Period']][Play['Down']][Play['YardsToGoClass']]:
                                            PlayTypeDict[Play['Period']][Play['Down']][Play['YardsToGoClass']][Play['BallSpotClass']] = {}
                                        if Play['LeadClass'] not in PlayTypeDict[Play['Period']][Play['Down']][Play['YardsToGoClass']][Play['BallSpotClass']]:
                                            PlayTypeDict[Play['Period']][Play['Down']][Play['YardsToGoClass']][Play['BallSpotClass']][Play['LeadClass']] = {}
                                        if Play['TimeLeftClass'] not in PlayTypeDict[Play['Period']][Play['Down']][Play['YardsToGoClass']][Play['BallSpotClass']][Play['LeadClass']]:
                                            PlayTypeDict[Play['Period']][Play['Down']][Play['YardsToGoClass']][Play['BallSpotClass']][Play['LeadClass']][Play['TimeLeftClass']] = {}

                                        PlayTypeTracker = PlayTypeDict[Play['Period']][Play['Down']][Play['YardsToGoClass']][Play['BallSpotClass']][Play['LeadClass']][Play['TimeLeftClass']]
                                        PlayTypeFound = False
                                        for PlayType in PlayTypeStrings:
                                            for EventString in PlayTypeStrings[PlayType]:
                                                if EventString.lower() in Play['Event'].lower() and not PlayTypeFound:
                                                    Play['PlayType'] = PlayType
                                                    PlayTypeFound = True
                                                    if Play['PlayType'] not in PlayTypeTracker:
                                                        PlayTypeTracker[Play['PlayType']] = 0
                                                    PlayTypeTracker[Play['PlayType']] +=1


                                        if PlayTypeFound == False:
                                            print('Couldnt find', Play['Event'])


                                        cleansed_data.append(Play)

                        else:
                            print('None table: ', GameNumber, 'GameNumber', Year, 'Year')
                    except:
                        pass

            with open('output/PlayTypeCounts-Year-'+str(Year)+'-Game-'+str(GameNumber)+'.json', 'w') as outfile:
                json.dump(PlayTypeDict, outfile)

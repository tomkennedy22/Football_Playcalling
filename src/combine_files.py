import glob
import json

def combine_json(Grouping='Year'):

    YearList = []
    for filepath in glob.iglob('output/*Game*.json'):
        filepath_split = filepath.split('-')

        Year = filepath_split[2]
        Week = filepath_split[4]

        if Year not in YearList:
            YearList.append(Year)

    print('YearList', YearList)

    if Grouping == 'Year': #TODO - make other groupings?
        for Year in YearList:
            MasterData = {}

            for filepath in glob.iglob('output/*Year-'+Year+'-Game*.json'):
                print(filepath)

                with open(filepath) as f:
                    WeekData = json.load(f)

                    for Period in WeekData:
                        if Period not in MasterData:
                            MasterData[Period] = {}
                        for Down in WeekData[Period]:
                            if Down not in MasterData[Period]:
                                MasterData[Period][Down] = {}
                            for YardsToGo in WeekData[Period][Down]:
                                if YardsToGo not in MasterData[Period][Down]:
                                    MasterData[Period][Down][YardsToGo] = {}
                                for BallSpot in WeekData[Period][Down][YardsToGo]:
                                    if BallSpot not in MasterData[Period][Down][YardsToGo]:
                                        MasterData[Period][Down][YardsToGo][BallSpot] = {}
                                    for Lead in WeekData[Period][Down][YardsToGo][BallSpot]:
                                        if Lead not in MasterData[Period][Down][YardsToGo][BallSpot]:
                                            MasterData[Period][Down][YardsToGo][BallSpot][Lead] = {}
                                        for TimeLeft in WeekData[Period][Down][YardsToGo][BallSpot][Lead]:
                                            if TimeLeft not in MasterData[Period][Down][YardsToGo][BallSpot][Lead]:
                                                MasterData[Period][Down][YardsToGo][BallSpot][Lead][TimeLeft] = {}
                                            for PlayType in WeekData[Period][Down][YardsToGo][BallSpot][Lead][TimeLeft]:
                                                if PlayType not in MasterData[Period][Down][YardsToGo][BallSpot][Lead][TimeLeft]:
                                                    MasterData[Period][Down][YardsToGo][BallSpot][Lead][TimeLeft][PlayType] = 0
                                                MasterData[Period][Down][YardsToGo][BallSpot][Lead][TimeLeft][PlayType] +=1


                    #1  Period
                    #2  Down
                    #3  YardsToGo
                    #4  BallSpot
                    #5  Lead
                    #6  TimeLeft
                    #7  PlayType

            with open('output/PlayTypeCounts-Year-'+str(Year)+'.json', 'w') as outfile:
                json.dump(MasterData, outfile)

from src.football_plays import get_gameplays




class Lead:

    def __init__(self, Floor = 0, Ceiling = 0):
        self.Floor = Floor
        self.Ceiling = Ceiling

    def __str__(self):
        s = ''
        if self.Floor < 0:
            s+= '!'
        s+=str(abs(self.Floor))

        s += '-'
        if self.Ceiling < 0:
            s+= '!'
        s+=str(abs(self.Ceiling))

        return s


class BallSpot:

    def __init__(self, Floor = 0, Ceiling = 0):
        self.Floor = Floor
        self.Ceiling = Ceiling

    def __str__(self):
        s = ''
        if self.Floor < 0:
            s+= '!'
        s+=str(abs(self.Floor))

        s += '-'
        if self.Ceiling < 0:
            s+= '!'
        s+=str(abs(self.Ceiling))

        return s


class YardsToGo:

    def __init__(self, Floor = 0, Ceiling = 0):
        self.Floor = Floor
        self.Ceiling = Ceiling

    def __str__(self):
        s = ''
        if self.Floor < 0:
            s+= '!'
        s+=str(abs(self.Floor))

        s += '-'
        if self.Ceiling < 0:
            s+= '!'
        s+=str(abs(self.Ceiling))

        return s


def MatchFloorCeiling(Val, Objs):
    print('Matching', Val)
    for ObjStr, Obj in Objs.items():
        if Val >= Obj.Floor and Val <= Obj.Ceiling:
            return Obj


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



print(Leads)
for u in range(-20,20):
    print(MatchLead(u, Leads))
#df = get_gameplays()

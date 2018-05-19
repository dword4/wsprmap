#!/usr/bin/python3

class HamLocation:

    def GetLon(self, ONE, THREE, FIVE):
        StrStartLon = ''
        StrEndLon = ''

        Field = ((ord(ONE.lower()) - 97) * 20) 
        Square = int(THREE) * 2
        SubSquareLow = (ord(FIVE.lower()) - 97) * (2/24)
        SubSquareHigh = SubSquareLow + (2/24)

        StrStartLon = str(Field + Square + SubSquareLow - 180 )
        StrEndLon = str(Field + Square + SubSquareHigh - 180 )

        return StrStartLon, StrEndLon

    def GetLat(self, TWO, FOUR, SIX):
        StrStartLat = ''
        StrEndLat = ''

        Field = ((ord(TWO.lower()) - 97) * 10) 
        Square = int(FOUR)
        SubSquareLow = (ord(SIX.lower()) - 97) * (1/24)
        SubSquareHigh = SubSquareLow + (1/24)

        StrStartLat = str(Field + Square + SubSquareLow - 90)
        StrEndLat = str(Field + Square + SubSquareHigh - 90)    

        return StrStartLat, StrEndLat

    def getCenter(self, strMaidenHead):
        if len(strMaidenHead) < 6: strMaidenHead = 'CN90TQ'

        ONE = strMaidenHead[0:1]
        TWO = strMaidenHead[1:2]
        THREE = strMaidenHead[2:3]
        FOUR = strMaidenHead[3:4]
        FIVE = strMaidenHead[4:5]
        SIX = strMaidenHead[5:6]

        (strStartLon, strEndLon) = self.GetLon(ONE, THREE, FIVE)
        (strStartLat, strEndLat) = self.GetLat(TWO, FOUR, SIX)

        centerLon = (float(strStartLon) + float(strEndLon)) / 2
        centerLat = (float(strStartLat) + float(strEndLat)) / 2
        
        return centerLat, centerLon


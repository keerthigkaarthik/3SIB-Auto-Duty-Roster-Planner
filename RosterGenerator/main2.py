from turtle import setundobuffer
from typing import final
from NSF import NSF
from NSF import S1
from NSF import S2
from NSF import S3
from NSF import S4
from NSF import HQCOY
from Day import days
import random
import csv
import os
import math
from decimal import Decimal

month = {

    'date': int,
    'name': str,
    'year': 2022,
    'totalDays': int,

    'allDays': [],

    'weekdays': 0,
    'fridays': 0,
    'weekends': 0,
    
    'totalPoints': 0,
    'totalNumberOfWeekends': 0,
    'totalShifts': 0,

    'averagePoints': 0,
    'averageNumberOfWeekends': 0,
    'averageShifts': 0,

    'AMWeekdayShifts': [],
    'PMWeekdayShifts': [],

    'fridayShifts': [],
    'AMWeekendShifts': [],
    'PMWeekendShifts': [],

    'totalPointsEarned': 0,
    'totalWkendsDone': 0,

    "balanceingpt": 0,
    "balanceingwked": 0


}

daysInAWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
monthsInAYear = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def generateMonth(monthDate:int, year:int, totalDays:int, firstDay:str):
    month['totalDays'] = totalDays
    month['date'] = monthDate
    month['name'] = monthsInAYear[month['date'] - 1]
    
    i = 1
    index = daysInAWeek.index(firstDay)
    while i <= totalDays:
        today = days(i, daysInAWeek[index%7])
        month['allDays'].append(today)


        if index%7 == 0 or index%7 == 1 or index%7 == 2 or index%7 == 3:
            month['weekdays']+= 1
            month['totalPoints']+= 1
            month['AMWeekdayShifts'].append(today)
            month['PMWeekdayShifts'].append(today)

        elif index%7 == 4:
            month['fridays']+= 1
            month['totalPoints']+= 1.5
            month['totalNumberOfWeekends']+= 0.5
            month['fridayShifts'].append(today)
            month['AMWeekdayShifts'].append(today)
            month['PMWeekendShifts'].append(today)

        elif index%7 == 5 or index%7 == 6:
            month['weekends']+= 1
            month['totalPoints']+= 2
            month['totalNumberOfWeekends']+= 1
            month['AMWeekendShifts'].append(today)
            month['PMWeekendShifts'].append(today)

        index+= 1
        i+= 1


def initNSF():
    with open('NSF.csv', 'r') as NSF_file:
        NSF_reader = csv.reader(NSF_file)
        for line in NSF_reader:
            if len(line)>8:
                if line[0] == '*':
                    if line[1] == 'S1':
                        S1(line[2], line[3] == "True", float(line[8]), float(line[9]))
                    elif line[1] == 'S2':
                        S2(line[2], line[3] == "True", float(line[8]), float(line[9]))
                    elif line[1] == 'S3':
                        S3(line[2], line[3] == "True", float(line[8]), float(line[9]))
                    elif line[1] == 'S4':
                        S4(line[2], line[3] == "True", float(line[8]), float(line[9]))
                    elif line[1] == 'HQCOY':
                        HQCOY(line[2], line[3] == "True", float(line[8]), float(line[9]))
            else:
                pass

def updateCommitment():
    with open('commitment.csv') as commitment_file:
        commitment_reader = csv.reader(commitment_file)

        next(commitment_reader)

        for line in commitment_reader:
            if len(line)>0:
                for boi in NSF.all:
                    if line[0] == boi.name:
                        listOfDays = line[1].split('/')
                        for e in listOfDays:
                            if '-' in e:
                                e = e.split('-')
                                i = int(e[0])
                                o = int(e[1])
                                while i <= o:
                                    boi.exclusionDays.append(i)
                                    i += 1
                            else:
                                boi.exclusionDays.append(int(e))
            else:
                pass
    

def updateExclusion():
    for boi in NSF.all:
        for d in boi.exclusionDays:
            month['allDays'][d-1].exclusion.append(boi.name)

def setDuty(who:str, when:int, shift:str):
    for nsf in NSF.all:
        if nsf.name == who:
            boi = nsf
    
    #when is the date as an integer
    d = month['allDays'][when-1]

    if shift == 'full' and boi.NightDuty == True:
        shiftType = 0
    elif shift == 'pm' and boi.NightDuty == True:
        shiftType = 1
    elif shift == 'am':
        shiftType = 2
    else:
        raise Exception("set duty shift type is wrong")


    d.exclusion.append(boi.name)
    boi.shifts_this_month += 1

    if d in month['fridayShifts']:
        month['fridayShifts'].remove(d)

    if shiftType == 0 or shiftType == 2:
        d.AMDC = boi
        boi.AMdates_served.append(d.date)

        if d in month['AMWeekdayShifts']:
            print(f"AM wkday set for {boi.name} on {d.date}")
            month['AMWeekdayShifts'].remove(d)
            boi.points += 0.5
            boi.points_earned_this_month += 0.5
        elif d in month['AMWeekendShifts']:
            print(f"AM wked set for {boi.name} on {d.date}")
            month['AMWeekendShifts'].remove(d)
            boi.points += 1
            boi.NoOfWkeds += 0.5
            boi.points_earned_this_month += 1
            boi.NoOfWkeds_done_this_month += 0.5
            
            
    if shiftType == 0 or shiftType == 1:
        d.PMDC = boi
        boi.PMdates_served.append(d.date)

        if d in month['PMWeekdayShifts']:
            print(f"PM wkday set for {boi.name} on {d.date}")
            month['PMWeekdayShifts'].remove(d)
            boi.points += 0.5
            boi.points_earned_this_month += 0.5
                
        elif d in month['PMWeekendShifts']:
            print(f"PM wked set for {boi.name} on {d.date}")
            month['PMWeekendShifts'].remove(d)
            boi.points += 1
            boi.NoOfWkeds += 0.5
            boi.points_earned_this_month += 1
            boi.NoOfWkeds_done_this_month += 0.5

        if d.date != 1 and d.date != len(month['allDays']):
            month['allDays'][d.date].exclusion.append(d.PMDC.name)
            month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
        elif d.date == 1:
            month['allDays'][d.date].exclusion.append(d.PMDC.name)
        elif d.date == len(month['allDays']):
            month['allDays'][d.date-2].exclusion.append(d.PMDC.name)

    
    if shiftType == 0:
        d.AMDC.AMdates_served.remove(d.date)
        d.AMDC.PMdates_served.remove(d.date)
        d.AMDC.fulldates_served.append(d.date)

def setExtra(who:str, when:int, shift:str):
    for nsf in NSF.all:
        if nsf.name == who:
            boi = nsf
    
    #when is the date as an integer
    d = month['allDays'][when-1]

    if shift == 'full' and boi.NightDuty == True:
        shiftType = 0
    elif shift == 'pm' and boi.NightDuty == True:
        shiftType = 1
    elif shift == 'am':
        shiftType = 2
    else:
        raise Exception("set duty shift type is wrong")

    d.exclusion.append(boi.name)

    if shiftType == 0 or shiftType == 2:
        d.AMDC = boi
        boi.extras_served.append(d.date)
        boi.shifts_this_month += 1 
        if d in month['AMWeekdayShifts']:
            month['totalPoints'] -= 0.5
            month['AMWeekdayShifts'].remove(d)
        elif d in month['AMWeekendShifts']:
            month['totalPoints'] -= 1
            month['totalNumberOfWeekends'] -= 0.5
            month['AMWeekendShifts'].remove(d)
        if d in month['PMWeekendShifts'] and shiftType == 2:
            PMavailable = NSF.night.copy()
            PMavailablecopy = PMavailable.copy()
            for guy in PMavailablecopy:
                if guy.name in d.exclusion:
                    PMavailable.remove(guy)
            PMavailable.sort(key = lambda guy:guy.NoOfWkeds)

            print(d.date)
            print(d.AMDC.name)
            
            if PMavailable == []:
                d.PMDC = random.choice(PMavailablecopy)
            else:
                d.PMDC = PMavailable[0]
            print(d.PMDC)
            d.PMDC.NoOfWkeds += 0.5
            d.PMDC.NoOfWkeds_done_this_month += 0.5
            d.PMDC.points += 1
            d.PMDC.points_earned_this_month += 1
            d.PMDC.shifts_this_month += 1

            d.PMDC.PMdates_served.append(d.date)

            d.exclusion.append(d.PMDC.name)
            if d.date != 1 and d.date != len(month['allDays']):
                month['allDays'][d.date].exclusion.append(d.PMDC.name)
                month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
            elif d.date == 1:
                month['allDays'][d.date].exclusion.append(d.PMDC.name)
            elif d.date == len(month['allDays']):
                month['allDays'][d.date-2].exclusion.append(d.PMDC.name)

            month['PMWeekendShifts'].remove(d)
        elif d in month['PMWeekdayShifts'] and shiftType == 2:
            PMavailable = NSF.night.copy()
            PMavailablecopy = PMavailable.copy()
            for guy in PMavailablecopy:
                if guy.name in d.exclusion:
                    PMavailable.remove(guy)
            PMavailable.sort(key = lambda guy:guy.points)
            
            if PMavailable == []:
                d.PMDC = random.choice(PMavailablecopy)
            else:
                d.PMDC = PMavailable[0]
            
            d.PMDC.points += 0.5
            d.PMDC.points_earned_this_month += 0.5
            d.PMDC.shifts_this_month += 1

            d.PMDC.PMdates_served.append(d.date)

            d.exclusion.append(d.PMDC.name)

            if d.date != 1 and d.date != len(month['allDays']):
                month['allDays'][d.date].exclusion.append(d.PMDC.name)
                month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
            elif d.date == 1:
                month['allDays'][d.date].exclusion.append(d.PMDC.name)
            elif d.date == len(month['allDays']):
                month['allDays'][d.date-2].exclusion.append(d.PMDC.name)

            month['PMWeekdayShifts'].remove(d)    
            
    if shiftType == 0 or shiftType == 1:
        d.PMDC = boi
        boi.extras_served.append(d.date)
        boi.shifts_this_month += 1
        if d in month['PMWeekdayShifts']:
            month['totalPoints'] -= 0.5
            month['PMWeekdayShifts'].remove(d)
                
        elif d in month['PMWeekendShifts']:
            month['totalPoints'] -= 1
            month['totalNumberOfWeekends'] -= 0.5
            month['PMWeekendShifts'].remove(d)
        
        if d.date != 1 and d.date != len(month['allDays']):
            month['allDays'][d.date].exclusion.append(d.PMDC.name)
            month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
        elif d.date == 1:
            month['allDays'][d.date].exclusion.append(d.PMDC.name)
        elif d.date == len(month['allDays']):
            month['allDays'][d.date-2].exclusion.append(d.PMDC.name)


def updateMonth():
    
    avept = month['totalPoints']/len(NSF.all)
    month['averagePoints'] = round(avept, 2)

    avewked = month['totalNumberOfWeekends']/len(NSF.all)
    month['averageNumberOfWeekends'] = round(avewked, 2)

    month['totalShifts'] = month['totalDays']*2
    month['averageShifts'] = round(month['totalShifts']/len(NSF.all))

    for boi in NSF.all:
        boi.points -= month['averagePoints']
        boi.NoOfWkeds -= month['averageNumberOfWeekends']

        boi.points = round(boi.points, 2)
        boi.NoOfWkeds = round(boi.NoOfWkeds, 2)
    

def clearAMonlyWKED():
    amlist = NSF.morning.copy()
    amlist.sort(key = lambda NSF:len(NSF.exclusionDays), reverse = True)
    for boi in amlist:
        if boi.NoOfWkeds > 0:
            continue
        else:
            AMwkeds = month['AMWeekendShifts'].copy()
            AMwkedscopy = AMwkeds.copy()
            for d in AMwkedscopy:
                if boi.name in d.exclusion:
                    AMwkeds.remove(d)
            if len(AMwkeds) == 0:
                continue
            AMwkeds.sort(key = lambda day: len(day.exclusion), reverse = True)
            AMwkedsreplica = AMwkeds.copy()
            for e in AMwkedsreplica:
                if e.PMDC != []:
                    AMwkeds.remove(e)
                    AMwkeds.insert(0, e)
            shiftsRequired = -math.floor(boi.NoOfWkeds/0.5)
            i = 0

            while i <shiftsRequired:
                if len(AMwkeds) == 0:
                   break
                d = AMwkeds[0]

                d.AMDC = boi
                d.AMDC.NoOfWkeds += 0.5
                d.AMDC.NoOfWkeds_done_this_month += 0.5
                d.AMDC.points += 1
                d.AMDC.points_earned_this_month += 1
                d.AMDC.shifts_this_month += 1

                d.AMDC.AMdates_served.append(d.date)
                
                AMwkeds.remove(d)
                month['AMWeekendShifts'].remove(d)

                d.exclusion.append(boi.name)
                if d.date != 1 and d.date != len(month['allDays']):
                        month['allDays'][d.date].exclusion.append(d.AMDC.name)
                        month['allDays'][d.date-2].exclusion.append(d.AMDC.name)
                elif d.date == 1:
                    month['allDays'][d.date].exclusion.append(d.AMDC.name)
                elif d.date == len(month['allDays']):
                    month['allDays'][d.date-2].exclusion.append(d.AMDC.name)

                if d in month['PMWeekendShifts']:
                    PMavailable = NSF.night.copy()
                    PMavailablecopy = PMavailable.copy()
                    for guy in PMavailablecopy:
                        if guy.name in d.exclusion:
                            PMavailable.remove(guy)
                    PMavailable.sort(key = lambda guy:guy.NoOfWkeds)

                    print(d.date)
                    print(d.AMDC.name)
                    
                    if PMavailable == []:
                        d.PMDC = random.choice(PMavailablecopy)
                    else:
                        d.PMDC = PMavailable[0]
                    print(d.PMDC)
                    d.PMDC.NoOfWkeds += 0.5
                    d.PMDC.NoOfWkeds_done_this_month += 0.5
                    d.PMDC.points += 1
                    d.PMDC.points_earned_this_month += 1
                    d.PMDC.shifts_this_month += 1

                    d.PMDC.PMdates_served.append(d.date)

                    d.exclusion.append(d.PMDC.name)
                    if d.date != 1 and d.date != len(month['allDays']):
                        month['allDays'][d.date].exclusion.append(d.PMDC.name)
                        month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
                    elif d.date == 1:
                        month['allDays'][d.date].exclusion.append(d.PMDC.name)
                    elif d.date == len(month['allDays']):
                        month['allDays'][d.date-2].exclusion.append(d.PMDC.name)

                    month['PMWeekendShifts'].remove(d)
                i += 1

def WKedFull():
    month['AMWeekendShifts'].sort(key = lambda day:len(day.exclusion), reverse = True)
    wkedsleft = month['AMWeekendShifts'].copy()
    for d in wkedsleft:
        if d in month['PMWeekendShifts']:
            FULLavailable = NSF.night.copy()
            FULLavailablecopy = FULLavailable.copy()
            for boi in FULLavailablecopy:
                if boi.name in d.exclusion:
                    FULLavailable.remove(boi)
            FULLavailable.sort(key = lambda boi:boi.NoOfWkeds)
            d.AMDC = FULLavailable[0]
            d.PMDC = FULLavailable[0]
            
            d.AMDC.NoOfWkeds += 1
            d.AMDC.NoOfWkeds_done_this_month += 1
            d.AMDC.points += 2
            d.AMDC.points_earned_this_month += 2
            d.AMDC.shifts_this_month += 2
            d.AMDC.fulldates_served.append(d.date)

            month['AMWeekendShifts'].remove(d)
            month['PMWeekendShifts'].remove(d)

            d.exclusion.append(d.AMDC.name)
            if d.date != 1 and d.date != len(month['allDays']):
                month['allDays'][d.date].exclusion.append(d.PMDC.name)
                month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
            elif d.date == 1:
                month['allDays'][d.date].exclusion.append(d.PMDC.name)
            elif d.date == len(month['allDays']):
                month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
        else:
            print(f'{d.date} is not in month[PMWeekendShifts]')

def FridayFull():
    month['fridayShifts'].sort(key = lambda day:len(day.exclusion), reverse = True)
    frisleft = month['fridayShifts'].copy()
    for d in frisleft:
        if d in month['PMWeekendShifts']:
            FULLavailable = NSF.night.copy()
            FULLavailablecopy = FULLavailable.copy()
            for boi in FULLavailablecopy:
                if boi.name in d.exclusion:
                    FULLavailable.remove(boi)
            FULLavailable.sort(key = lambda boi:boi.NoOfWkeds)
            d.AMDC = FULLavailable[0]
            d.PMDC = FULLavailable[0]
            
            d.AMDC.NoOfWkeds += 0.5
            d.AMDC.NoOfWkeds_done_this_month += 0.5
            d.AMDC.points += 1.5
            d.AMDC.points_earned_this_month += 1.5
            d.AMDC.shifts_this_month += 2
            d.AMDC.fulldates_served.append(d.date)

            month['AMWeekdayShifts'].remove(d)
            month['PMWeekendShifts'].remove(d)
            month['fridayShifts'].remove(d)

            d.exclusion.append(d.AMDC.name)
            if d.date != 1 and d.date != len(month['allDays']):
                month['allDays'][d.date].exclusion.append(d.PMDC.name)
                month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
            elif d.date == 1:
                month['allDays'][d.date].exclusion.append(d.PMDC.name)
            elif d.date == len(month['allDays']):
                month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
        else:
            print(f'{d.date} is not in month[PMWeekendShifts]')

def clearAMonlyWKDAY():
    amlist = NSF.morning.copy()
    amlist.sort(key = lambda NSF:len(NSF.exclusionDays), reverse = True)
    for boi in amlist:
        if boi.points > 0:
            continue
        else:
            AMwkdays = month['AMWeekdayShifts'].copy()
            AMwkdayscopy = AMwkdays.copy()
            for d in AMwkdayscopy:
                if boi.name in d.exclusion:
                    AMwkdays.remove(d)
            if len(AMwkdays) == 0:
                continue
            
            AMwkdays.sort(key = lambda day: len(day.exclusion), reverse = True)
            AMwkdaysreplica = AMwkdays.copy()
            for e in AMwkdaysreplica:
                if e.PMDC != []:
                    AMwkdays.remove(e)
                    AMwkdays.insert(0, e)
            
            shiftsRequired = -math.floor(boi.points/0.5)
            i = 0

            while i <shiftsRequired:
                if len(AMwkdays) == 0:
                   break
                
                d = AMwkdays[0]
                d.AMDC = boi
                d.AMDC.points += 0.5
                d.AMDC.points_earned_this_month += 0.5
                d.AMDC.shifts_this_month += 1

                d.AMDC.AMdates_served.append(d.date)

                AMwkdays.remove(d)
                month['AMWeekdayShifts'].remove(d)
                if d in month['fridayShifts']:
                    month['fridayShifts'].remove(d)

                d.exclusion.append(boi.name)
                if d.date != 1 and d.date != len(month['allDays']):
                        month['allDays'][d.date].exclusion.append(d.AMDC.name)
                        month['allDays'][d.date-2].exclusion.append(d.AMDC.name)
                elif d.date == 1:
                    month['allDays'][d.date].exclusion.append(d.AMDC.name)
                elif d.date == len(month['allDays']):
                    month['allDays'][d.date-2].exclusion.append(d.AMDC.name)

                if d in month['PMWeekendShifts']:
                    PMavailable = NSF.night.copy()
                    PMavailablecopy = PMavailable.copy()
                    for guy in PMavailablecopy:
                        if guy.name in d.exclusion:
                            PMavailable.remove(guy)
                    PMavailable.sort(key = lambda guy:guy.NoOfWkeds)
                    
                    if PMavailable == []:
                        d.PMDC = random.choice(PMavailablecopy)
                    else:
                        d.PMDC = PMavailable[0]
                    d.PMDC.NoOfWkeds += 0.5
                    d.PMDC.NoOfWkeds_done_this_month += 0.5
                    d.PMDC.points += 1
                    d.PMDC.points_earned_this_month += 1
                    d.PMDC.shifts_this_month += 1

                    d.PMDC.PMdates_served.append(d.date)

                    d.exclusion.append(d.PMDC.name)

                    if d.date != 1 and d.date != len(month['allDays']):
                        month['allDays'][d.date].exclusion.append(d.PMDC.name)
                        month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
                    elif d.date == 1:
                        month['allDays'][d.date].exclusion.append(d.PMDC.name)
                    elif d.date == len(month['allDays']):
                        month['allDays'][d.date-2].exclusion.append(d.PMDC.name)

                    month['PMWeekendShifts'].remove(d)
                elif d in month['PMWeekdayShifts']:
                    PMavailable = NSF.night.copy()
                    PMavailablecopy = PMavailable.copy()
                    for guy in PMavailablecopy:
                        if guy.name in d.exclusion:
                            PMavailable.remove(guy)
                    PMavailable.sort(key = lambda guy:guy.points)
                    
                    if PMavailable == []:
                        d.PMDC = random.choice(PMavailablecopy)
                    else:
                        d.PMDC = PMavailable[0]
                    
                    d.PMDC.points += 0.5
                    d.PMDC.points_earned_this_month += 0.5
                    d.PMDC.shifts_this_month += 1

                    d.PMDC.PMdates_served.append(d.date)

                    d.exclusion.append(d.PMDC.name)

                    if d.date != 1 and d.date != len(month['allDays']):
                        month['allDays'][d.date].exclusion.append(d.PMDC.name)
                        month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
                    elif d.date == 1:
                        month['allDays'][d.date].exclusion.append(d.PMDC.name)
                    elif d.date == len(month['allDays']):
                        month['allDays'][d.date-2].exclusion.append(d.PMDC.name)

                    month['PMWeekdayShifts'].remove(d)
                    

                i += 1

def WKdayFull():
    month['AMWeekdayShifts'].sort(key = lambda day:len(day.exclusion), reverse = True)
    wkdaysleft = month['AMWeekdayShifts'].copy()
    for d in wkdaysleft:
        if d in month['PMWeekdayShifts']:
            FULLavailable = NSF.night.copy()
            FULLavailablecopy = FULLavailable.copy()
            for boi in FULLavailablecopy:
                if boi.name in d.exclusion:
                    FULLavailable.remove(boi)
            
            FULLavailable.sort(key = lambda boi:boi.points)
            d.AMDC = FULLavailable[0]
            d.PMDC = d.AMDC
            
            d.AMDC.points += 1
            d.AMDC.points_earned_this_month += 1
            d.AMDC.shifts_this_month += 2
            d.AMDC.fulldates_served.append(d.date)

            month['AMWeekdayShifts'].remove(d)
            month['PMWeekdayShifts'].remove(d)

            d.exclusion.append(d.AMDC.name)
            if d.date != 1 and d.date != len(month['allDays']):
                month['allDays'][d.date].exclusion.append(d.PMDC.name)
                month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
            elif d.date == 1:
                month['allDays'][d.date].exclusion.append(d.PMDC.name)
            elif d.date == len(month['allDays']):
                month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
        else:
            print(f'{d.date} is not in month[PMWeekdayShifts]')

def reserveSelection():
    for d in month['allDays']:

        PMbr = d.PMDC.__class__.__name__
        if PMbr == 'S1':
            PMreserveList = S1.night.copy()
        elif PMbr == 'S2':
            PMreserveList = S2.night.copy()
        elif PMbr == 'S3':
            PMreserveList = S3.night.copy()
        elif PMbr == 'S4':
            PMreserveList = S4.night.copy()
        elif PMbr == 'HQCOY':
            PMreserveList = HQCOY.night.copy()

        PMreserveListcopy = PMreserveList.copy()
        for boi in PMreserveListcopy:
                if boi.name in d.exclusion:
                    PMreserveList.remove(boi)

        if d.AMDC == d.PMDC:
            if month['allDays'][d.date-2].PMDC in PMreserveList:
                PMreserveList.remove(month['allDays'][d.date-2].PMDC)
            if month['allDays'][d.date-2].AMDC in PMreserveList:
                PMreserveList.remove(month['allDays'][d.date-2].AMDC)
            if month['allDays'][d.date].PMDC in PMreserveList:
                PMreserveList.remove(month['allDays'][d.date].PMDC)
            if month['allDays'][d.date].AMDC in PMreserveList:
                PMreserveList.remove(month['allDays'][d.date].AMDC)
    
            if PMreserveList != []:
                pass
            else:
                PMreserveList = NSF.night.copy()
                for boi in d.PMreserveList:
                    if boi.name in d.exclusion:
                        PMreserveList.remove(boi)
                if month['allDays'][d.date-2].PMDC in PMreserveList:
                    PMreserveList.remove(month['allDays'][d.date-2].PMDC)
                if month['allDays'][d.date-2].AMDC in PMreserveList:
                    PMreserveList.remove(month['allDays'][d.date-2].AMDC)
                if month['allDays'][d.date].PMDC in PMreserveList:
                    PMreserveList.remove(month['allDays'][d.date].PMDC)
                if month['allDays'][d.date].AMDC in PMreserveList:
                    PMreserveList.remove(month['allDays'][d.date].AMDC)
            
            d.AMreserve = random.choice(PMreserveList)
            d.PMreserve = d.AMreserve
            d.AMreserve.reservedates.append(d.date)
        else:
            AMbr = d.AMDC.__class__.__name__
            if AMbr == 'S1':
                AMreserveList = S1.all.copy()
            elif AMbr == 'S2':
                AMreserveList = S2.all.copy()
            elif AMbr == 'S3':
                AMreserveList = S3.all.copy()
            elif AMbr == 'S4':
                AMreserveList = S4.all.copy()
            elif AMbr == 'HQCOY':
                AMreserveList = HQCOY.all.copy()

            AMreserveListcopy = AMreserveList.copy()

            for boi in AMreserveListcopy:
                if boi.name in d.exclusion:
                    AMreserveList.remove(boi)

            if AMreserveList != []:
                pass
            else:
                AMreserveList = NSF.all.copy()
                for boi in AMreserveList:
                    if boi.name in d.exclusion:
                        AMreserveList.remove(boi)
                
            d.AMreserve = random.choice(AMreserveList)
            d.AMreserve.reservedates.append(d.date)
            
            if PMreserveList != []:
                pass
            else:
                PMreserveList = NSF.night.copy()
                for boi in d.PMreserveList:
                    if boi.name in d.exclusion:
                        PMreserveList.remove(boi)
            d.PMreserve = random.choice(PMreserveList)
            d.PMreserve.reservedates.append(d.date)

def reserveselector2():
    for d in month['allDays']:
        reserveavail = NSF.all.copy()
        for boi in NSF.all:
            if boi.name in d.exclusion or len(boi.reservedates) > 2:
                reserveavail.remove(boi)
        if reserveavail != []:
            d.AMreserve = random.choice(reserveavail)
            d.AMreserve.reservedates.append(d.date)
        else: 
            d.AMreserve = random.choice(NSF.all)
            d.AMreserve.reservedates.append(d.date)
        if d.date < len(month['allDays']):
            month['allDays'][d.date].exclusion.append(d.AMreserve.name)
        if d.AMreserve.NightDuty:
            d.PMreserve = d.AMreserve
        else:
            nightReserveAvail = NSF.night.copy()
            for boi in NSF.night:
                if boi.name in d.exclusion or len(boi.reservedates) > 3:
                    nightReserveAvail.remove(boi)
            if nightReserveAvail != []:
                d.PMreserve = random.choice(nightReserveAvail)
                d.PMreserve.reservedates.append(d.date)
            else: 
                d.PMreserve = random.choice(NSF.night)
                d.PMreserve.reservedates.append(d.date)
            if d.date < len(month['allDays']):
                month['allDays'][d.date].exclusion.append(d.PMreserve.name)


def checker():
    for boi in NSF.all:
        for d in boi.exclusionDays:
            if month['allDays'][d-1].AMDC == boi or month['allDays'][d-1].PMDC == boi or month['allDays'][d-1].AMreserve == boi or month['allDays'][d-1].PMreserve == boi:
                print(f'Alert! {boi.name} is set for {d} even though he has commitments')
    
    for d in month['allDays']:
        print(f"Checking {d.date}")
        if d.PMDC.NightDuty:
            pass
        else:
            print(d.PMDC.NightDuty)
            print(f"Alert! {d.PMDC.name} is scheduled for night duty on {d.date} even though he is excused")
        if d.PMreserve.NightDuty:
            pass
        else:
            print(f"Alert! {d.PMreserve.name} is reserve for night duty on {d.date} even though he is excused")
        
        if d.AMDC == d.AMreserve:
            print(f"Alert! {d.AMDC.name} is AM main and reserve for {d.date}")
        if d.PMDC == d.PMreserve:
            print(f"Alert! {d.PMDC.name} is PM main and reserve for {d.date}")

        if d.AMDC == d.PMDC:
            if d.date > 1 and d.date < len(month['allDays']):
                if d.AMDC == month['allDays'][d.date].AMDC or d.AMDC == month['allDays'][d.date-2].PMDC:
                    print(f"Alert! {d.AMDC.name} is doing more than 24hrs on {d.date}")
                if d.AMDC == month['allDays'][d.date].AMreserve or d.AMDC == month['allDays'][d.date-2].PMreserve:
                    print(f"Alert! {d.AMDC.name} is reserve before/after 24hrs on {d.date}")
        
        if d.AMreserve == d.PMreserve:
            if d.date > 1 and d.date < len(month['allDays']):
                if d.AMreserve == month['allDays'][d.date].AMDC or d.AMreserve == month['allDays'][d.date-2].PMDC:
                    print(f"Alert! {d.AMDC.name} is reserve for 24hrs before/after another shift on {d.date}")
                if d.AMreserve == month['allDays'][d.date].AMreserve or d.AMreserve == month['allDays'][d.date-2].PMreserve:
                    print(f"Alert! {d.AMDC.name} is reserve for 24hrs before/after on {d.date}")

    
    for guy in NSF.all:
        month['totalPointsEarned'] += guy.points_earned_this_month
        month['totalWkendsDone'] += guy.NoOfWkeds_done_this_month

        
    if month['totalPointsEarned'] != month['totalPoints']:
        print("Something is not adding up (points)")
    if month['totalWkendsDone'] != month['totalNumberOfWeekends']:
        print(month['totalWkendsDone'])
        print(month['totalNumberOfWeekends'])
        print("Something is not adding up (wkeds)")

def printPoints():
    with open('points.csv', 'w') as points_file:
        points_writer = csv.writer(points_file)

        points_writer.writerow(["f*f",'branch', 'name', 'nightduty', 'points from last month', 'no. of wkends last month', 'points earned this month', 'no. of wkends this month', 'total points', 'total no. of wkends'])

        points_writer.writerow(" ")
        points_writer.writerow([f"Total points: {month['totalPoints']}", f"Total points: {month['totalNumberOfWeekends']}", f"Average points: {month['averagePoints']}", f"Average wkeds: {month['averageNumberOfWeekends']}", f"Balanced points: {month['balanceingpt']}", f"Balanced wkeds: {month['balanceingwked']}"])
        #points_writer.writerow([f"Total points: {month['totalNumberOfWeekends']}"])
        #points_writer.writerow([f"Average points: {month['averagePoints']}"])
        #points_writer.writerow([f"Average wkeds: {month['averageNumberOfWeekends']}"])

        points_writer.writerow(" ")
        points_writer.writerow(" ")
        points_writer.writerow(["S1 Branch:"])
        for boi in S1.all:
            points_writer.writerow(['*','S1', f'{boi.name}', f'{boi.NightDuty}', f'{boi.points_from_last_month}', f'{boi.NoOfWkeds_from_last_month}', f'{boi.points_earned_this_month}', f'{boi.NoOfWkeds_done_this_month}', f'{boi.points}', f'{boi.NoOfWkeds}'])

        points_writer.writerow(" ")
        points_writer.writerow(" ")
        points_writer.writerow(["S2 Branch:"])
        for boi in S2.all:
            points_writer.writerow(['*','S2', f'{boi.name}', f'{boi.NightDuty}', f'{boi.points_from_last_month}', f'{boi.NoOfWkeds_from_last_month}', f'{boi.points_earned_this_month}', f'{boi.NoOfWkeds_done_this_month}', f'{boi.points}', f'{boi.NoOfWkeds}'])

        points_writer.writerow(" ")
        points_writer.writerow(" ")
        points_writer.writerow(["S3 Branch:"])
        for boi in S3.all:
            points_writer.writerow(['*','S3', f'{boi.name}', f'{boi.NightDuty}', f'{boi.points_from_last_month}', f'{boi.NoOfWkeds_from_last_month}', f'{boi.points_earned_this_month}', f'{boi.NoOfWkeds_done_this_month}', f'{boi.points}', f'{boi.NoOfWkeds}'])

        points_writer.writerow(" ")
        points_writer.writerow(" ")
        points_writer.writerow(["S4 Branch:"])
        for boi in S4.all:
            points_writer.writerow(['*','S4', f'{boi.name}', f'{boi.NightDuty}', f'{boi.points_from_last_month}', f'{boi.NoOfWkeds_from_last_month}', f'{boi.points_earned_this_month}', f'{boi.NoOfWkeds_done_this_month}', f'{boi.points}', f'{boi.NoOfWkeds}'])

       
        points_writer.writerow(" ")
        points_writer.writerow(" ")
        points_writer.writerow(["HQCOY Branch:"])
        for boi in HQCOY.all:
            points_writer.writerow(['*','HQCOY', f'{boi.name}', f'{boi.NightDuty}', f'{boi.points_from_last_month}', f'{boi.NoOfWkeds_from_last_month}', f'{boi.points_earned_this_month}', f'{boi.NoOfWkeds_done_this_month}', f'{boi.points}', f'{boi.NoOfWkeds}'])

def printDates():
    with open('dates.csv', 'w') as dates_file:
        dates_writer = csv.writer(dates_file)

        dates_writer.writerow(['f*f', 'name', 'AM_Shifts_Dates', 'PM_Shift_dates', 'Full_Shift_dates', 'reserve_dates', 'extras'])
        dates_writer.writerow([f"Average shifts: {month['averageShifts']}"])

        dates_writer.writerow(" ")
        dates_writer.writerow(" ")
        for boi in S1.all:
            dates_writer.writerow(["S1", f'{boi.name}', f'{boi.AMdates_served}', f'{boi.PMdates_served}', f'{boi.fulldates_served}', f'{boi.reservedates}', f'{boi.extras_served}'])

        dates_writer.writerow(" ")
        dates_writer.writerow(" ")
        for boi in S2.all:
            dates_writer.writerow(["S2", f'{boi.name}', f'{boi.AMdates_served}', f'{boi.PMdates_served}', f'{boi.fulldates_served}', f'{boi.reservedates}', f'{boi.extras_served}'])
        
        dates_writer.writerow(" ")
        dates_writer.writerow(" ")
        for boi in S3.all:
            dates_writer.writerow(["S3", f'{boi.name}', f'{boi.AMdates_served}', f'{boi.PMdates_served}', f'{boi.fulldates_served}', f'{boi.reservedates}', f'{boi.extras_served}'])
        
        dates_writer.writerow(" ")
        dates_writer.writerow(" ")
        for boi in S4.all:
            dates_writer.writerow(["S4", f'{boi.name}', f'{boi.AMdates_served}', f'{boi.PMdates_served}', f'{boi.fulldates_served}', f'{boi.reservedates}', f'{boi.extras_served}'])
        
        dates_writer.writerow(" ")
        dates_writer.writerow(" ")
        for boi in HQCOY.all:
            dates_writer.writerow(["HQCOY", f'{boi.name}', f'{boi.AMdates_served}', f'{boi.PMdates_served}', f'{boi.fulldates_served}', f'{boi.reservedates}', f'{boi.extras_served}'])


def printRoster():
    with open('roster.csv', 'w') as roster_file:
        currmon = month['name']
        roster_writer = csv.writer(roster_file)

        for hi in month['allDays']:
            roster_writer.writerow([f'{currmon}, {hi.date}, {hi.day}'])
            roster_writer.writerow([f'AM main: {hi.AMDC.name}'])
            roster_writer.writerow([f'AM reserve: {hi.AMreserve.name}'])
            roster_writer.writerow([f'PM main: {hi.PMDC.name}'])
            roster_writer.writerow([f'PM reserve: {hi.PMreserve.name}'])
            roster_writer.writerow(" ")


def rosterPrinter2():
    with open('schedule.csv', 'w') as roster_file:
        currmon = month['name']
        year = month['year']
        alldays = month['allDays']
        roster_writer = csv.writer(roster_file)

        roster_writer.writerow([f'{currmon}', f'{year}', '', '', '', '', '', '',])
        roster_writer.writerow([" ", f'{alldays[0].day}', f'{alldays[1].day}', f'{alldays[2].day}', f'{alldays[3].day}', f'{alldays[4].day}', f'{alldays[5].day}', f'{alldays[6].day}'])
        roster_writer.writerow([" ", f'{alldays[0].date}', f'{alldays[1].date}', f'{alldays[2].date}', f'{alldays[3].date}', f'{alldays[4].date}', f'{alldays[5].date}', f'{alldays[6].date}'])
        roster_writer.writerow(["AM Main:", f'{alldays[0].AMDC.name}', f'{alldays[1].AMDC.name}', f'{alldays[2].AMDC.name}', f'{alldays[3].AMDC.name}', f'{alldays[4].AMDC.name}', f'{alldays[5].AMDC.name}', f'{alldays[6].AMDC.name}'])
        roster_writer.writerow(["PM Main:", f'{alldays[0].PMDC.name}', f'{alldays[1].PMDC.name}', f'{alldays[2].PMDC.name}', f'{alldays[3].PMDC.name}', f'{alldays[4].PMDC.name}', f'{alldays[5].PMDC.name}', f'{alldays[6].PMDC.name}'])
        roster_writer.writerow(" ")
        roster_writer.writerow(["AM Reserve:", f'{alldays[0].AMreserve.name}', f'{alldays[1].AMreserve.name}', f'{alldays[2].AMreserve.name}', f'{alldays[3].AMreserve.name}', f'{alldays[4].AMreserve.name}', f'{alldays[5].AMreserve.name}', f'{alldays[6].AMreserve.name}'])
        roster_writer.writerow(["PM Reserve:", f'{alldays[0].PMreserve.name}', f'{alldays[1].PMreserve.name}', f'{alldays[2].PMreserve.name}', f'{alldays[3].PMreserve.name}', f'{alldays[4].PMreserve.name}', f'{alldays[5].PMreserve.name}', f'{alldays[6].PMreserve.name}'])
        roster_writer.writerow(" ")

        roster_writer.writerow([" ", f'{alldays[7].date}', f'{alldays[8].date}', f'{alldays[9].date}', f'{alldays[10].date}', f'{alldays[11].date}', f'{alldays[12].date}', f'{alldays[13].date}'])
        roster_writer.writerow(["AM Main:", f'{alldays[7].AMDC.name}', f'{alldays[8].AMDC.name}', f'{alldays[9].AMDC.name}', f'{alldays[10].AMDC.name}', f'{alldays[11].AMDC.name}', f'{alldays[12].AMDC.name}', f'{alldays[13].AMDC.name}'])
        roster_writer.writerow(["PM Main:", f'{alldays[7].PMDC.name}', f'{alldays[8].PMDC.name}', f'{alldays[9].PMDC.name}', f'{alldays[10].PMDC.name}', f'{alldays[11].PMDC.name}', f'{alldays[12].PMDC.name}', f'{alldays[13].PMDC.name}'])
        roster_writer.writerow(" ")
        roster_writer.writerow(["AM Reserve:", f'{alldays[7].AMreserve.name}', f'{alldays[8].AMreserve.name}', f'{alldays[9].AMreserve.name}', f'{alldays[10].AMreserve.name}', f'{alldays[11].AMreserve.name}', f'{alldays[12].AMreserve.name}', f'{alldays[13].AMreserve.name}'])
        roster_writer.writerow(["PM Reserve:", f'{alldays[7].PMreserve.name}', f'{alldays[8].PMreserve.name}', f'{alldays[9].PMreserve.name}', f'{alldays[10].PMreserve.name}', f'{alldays[11].PMreserve.name}', f'{alldays[12].PMreserve.name}', f'{alldays[13].PMreserve.name}'])
        roster_writer.writerow(" ")

        roster_writer.writerow([" ", f'{alldays[14].date}', f'{alldays[15].date}', f'{alldays[16].date}', f'{alldays[17].date}', f'{alldays[18].date}', f'{alldays[19].date}', f'{alldays[20].date}'])
        roster_writer.writerow(["AM Main:", f'{alldays[14].AMDC.name}', f'{alldays[15].AMDC.name}', f'{alldays[16].AMDC.name}', f'{alldays[17].AMDC.name}', f'{alldays[18].AMDC.name}', f'{alldays[19].AMDC.name}', f'{alldays[20].AMDC.name}'])
        roster_writer.writerow(["PM Main:", f'{alldays[14].PMDC.name}', f'{alldays[15].PMDC.name}', f'{alldays[16].PMDC.name}', f'{alldays[17].PMDC.name}', f'{alldays[18].PMDC.name}', f'{alldays[19].PMDC.name}', f'{alldays[20].PMDC.name}'])
        roster_writer.writerow(" ")
        roster_writer.writerow(["AM Reserve:", f'{alldays[14].AMreserve.name}', f'{alldays[15].AMreserve.name}', f'{alldays[16].AMreserve.name}', f'{alldays[17].AMreserve.name}', f'{alldays[18].AMreserve.name}', f'{alldays[19].AMreserve.name}', f'{alldays[20].AMreserve.name}'])
        roster_writer.writerow(["PM Reserve:", f'{alldays[14].PMreserve.name}', f'{alldays[15].PMreserve.name}', f'{alldays[16].PMreserve.name}', f'{alldays[17].PMreserve.name}', f'{alldays[18].PMreserve.name}', f'{alldays[19].PMreserve.name}', f'{alldays[20].PMreserve.name}'])
        roster_writer.writerow(" ")

        roster_writer.writerow([" ", f'{alldays[21].date}', f'{alldays[22].date}', f'{alldays[23].date}', f'{alldays[24].date}', f'{alldays[25].date}', f'{alldays[26].date}', f'{alldays[27].date}'])
        roster_writer.writerow(["AM Main:", f'{alldays[21].AMDC.name}', f'{alldays[22].AMDC.name}', f'{alldays[23].AMDC.name}', f'{alldays[24].AMDC.name}', f'{alldays[25].AMDC.name}', f'{alldays[26].AMDC.name}', f'{alldays[27].AMDC.name}'])
        roster_writer.writerow(["PM Main:", f'{alldays[21].PMDC.name}', f'{alldays[22].PMDC.name}', f'{alldays[23].PMDC.name}', f'{alldays[24].PMDC.name}', f'{alldays[25].PMDC.name}', f'{alldays[26].PMDC.name}', f'{alldays[27].PMDC.name}'])
        roster_writer.writerow(" ")
        roster_writer.writerow(["AM Reserve:", f'{alldays[21].AMreserve.name}', f'{alldays[22].AMreserve.name}', f'{alldays[23].AMreserve.name}', f'{alldays[24].AMreserve.name}', f'{alldays[25].AMreserve.name}', f'{alldays[26].AMreserve.name}', f'{alldays[27].AMreserve.name}'])
        roster_writer.writerow(["PM Reserve:", f'{alldays[21].PMreserve.name}', f'{alldays[22].PMreserve.name}', f'{alldays[23].PMreserve.name}', f'{alldays[24].PMreserve.name}', f'{alldays[25].PMreserve.name}', f'{alldays[26].PMreserve.name}', f'{alldays[27].PMreserve.name}'])
        roster_writer.writerow(" ")

        if len(month['allDays']) == 29:
            roster_writer.writerow([" ", f'{alldays[28].date}'])
            roster_writer.writerow(["AM Main:", f'{alldays[28].AMDC.name}'])
            roster_writer.writerow(["PM Main:", f'{alldays[28].PMDC.name}'])
            roster_writer.writerow(" ")
            roster_writer.writerow(["AM Reserve:", f'{alldays[28].AMreserve.name}'])
            roster_writer.writerow(["PM Reserve:", f'{alldays[28].PMreserve.name}'])
            roster_writer.writerow(" ")
        elif len(month['allDays']) == 30:
            roster_writer.writerow([" ", f'{alldays[28].date}', f'{alldays[29].date}'])
            roster_writer.writerow(["AM Main:", f'{alldays[28].AMDC.name}', f'{alldays[29].AMDC.name}'])
            roster_writer.writerow(["PM Main:", f'{alldays[28].PMDC.name}', f'{alldays[29].PMDC.name}'])
            roster_writer.writerow(" ")
            roster_writer.writerow(["AM Reserve:", f'{alldays[28].AMreserve.name}', f'{alldays[29].AMreserve.name}'])
            roster_writer.writerow(["PM Reserve:", f'{alldays[28].PMreserve.name}', f'{alldays[29].PMreserve.name}'])
            roster_writer.writerow(" ")
        elif len(month['allDays']) == 31:
            roster_writer.writerow([" ", f'{alldays[28].date}', f'{alldays[29].date}', f'{alldays[30].date}'])
            roster_writer.writerow(["AM Main:", f'{alldays[28].AMDC.name}', f'{alldays[29].AMDC.name}', f'{alldays[30].AMDC.name}'])
            roster_writer.writerow(["PM Main:", f'{alldays[28].PMDC.name}', f'{alldays[29].PMDC.name}', f'{alldays[30].PMDC.name}'])
            roster_writer.writerow(" ")
            roster_writer.writerow(["AM Reserve:", f'{alldays[28].AMreserve.name}', f'{alldays[29].AMreserve.name}', f'{alldays[30].AMreserve.name}'])
            roster_writer.writerow(["PM Reserve:", f'{alldays[28].PMreserve.name}', f'{alldays[29].PMreserve.name}', f'{alldays[30].PMreserve.name}'])
            roster_writer.writerow(" ")
        else:
            print("Srry! Smth fked up. Line:878")


def fullgenerate(monthDate:int, year:int, totalDays:int, firstDay:str):

    generateMonth(monthDate, year, totalDays, firstDay)
    initNSF()
    updateCommitment()

    updateExclusion()
    updateMonth()

    setExtra("Jun Hao", 3, "full")
    

    print('start clearAMonlyWKED')    
    clearAMonlyWKED()
    print('end clearAMonlyWKED')
    print()  

    print('start WKedFull')
    WKedFull()
    print('end WKedFull') 
    print() 

    print('start FriFull')
    FridayFull()
    print('end FriFull')
    print()

    print('start clearAMonlyWKDAY')
    clearAMonlyWKDAY()
    print('end clearAMonlyWKDAY')
    print() 

    print('start WKdayFull')
    WKdayFull()
    print('end WKdayFull')
    print() 

    for kid in NSF.all:
        kid.points = round(kid.points, 2)
        kid.NoOfWkeds = round(kid.NoOfWkeds, 2)


    if month['date']%3 == 0:
        totalpt = 0
        totalwked = 0
        for boi in NSF.all:
            totalpt += boi.points
            totalwked += boi.NoOfWkeds
        
        
        month["balanceingpt"] = totalpt/len(NSF.all)
        month["balanceingpt"] = round(month["balanceingpt"], 2)
        month["balanceingwked"] = totalwked/len(NSF.all)
        month["balanceingwked"] = round(month["balanceingwked"], 2)

        for boi in NSF.all:
            boi.points -= month["balanceingpt"]
            boi.NoOfWkeds -= month["balanceingwked"]

            boi.points = round(boi.points, 2)
            boi.NoOfWkeds = round(boi.NoOfWkeds, 2)

        finaltotalpt = 0
        finaltotalwk = 0
        for boi in NSF.all:
            finaltotalpt += boi.points
            finaltotalwk += boi.NoOfWkeds
            print(finaltotalpt)
            print(finaltotalwk)

    #reserveSelection()
    reserveselector2()

    checker()

    printPoints()
    printDates()
    printRoster()
    rosterPrinter2()


fullgenerate(12, 2022, 31, "Thursday")
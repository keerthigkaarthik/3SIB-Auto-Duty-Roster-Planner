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
    'PMWeekendShifts': []


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


def updateExclusion():
    for boi in NSF.all:
        for d in boi.exclusionDays:
            month['allDays'][d-1].exclusion.append(boi.name)

def PMWEselection():
    month['PMWeekendShifts'].sort(key = lambda day:len(day.exclusion))
    for d in month['PMWeekendShifts']:
        d.PMavailable = NSF.night.copy()
        for boi in d.PMavailable:
            for name in d.exclusion:
                if boi.name == name:
                    d.PMavailble.remove(boi)
        d.PMavailable.sort(key = lambda boi:boi.NoOfWkeds)
        d.PMDC = d.PMavailable[0]
        d.PMavailable.remove(d.PMDC)
        d.PMDC.NoOfWkeds += 0.5
        d.PMDC.points += 1

        if d.date != 1 or d.date != len(month['allDays']):
            month['allDays'][d.date].exclusion.append(d.PMDC.name)
            month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
        elif d.date == 1:
            month['allDays'][d.date].exclusion.append(d.PMDC.name)
        elif d.date == len(month['allDays']):
            month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
        
        d.PMDC.points_earned_this_month += 1
        d.PMDC.NoOfWkeds_done_this_month += 0.5
        d.PMDC.shifts_this_month += 1
        d.PMDC.PMdates_served.append(d.date)

        month['totalPoints'] += 1
        month['totalNumberOfWeekends'] += 0.5

def AMWEselection():
    month['AMWeekendShifts'].sort(key = lambda day:len(day.exclusion))
    for d in month['AMWeekendShifts']:
        d.available = NSF.all.copy()
        for boi in d.available:
            for name in d.exclusion:
                if boi.name == name:
                    d.availble.remove(boi)
        d.available.sort(key = lambda boi:boi.NoOfWkeds)
        d.AMDC = d.available[0]
        d.available.remove(d.AMDC)
        d.AMDC.NoOfWkeds += 0.5
        d.AMDC.points += 1

        if d.date != 1 or d.date != len(month['allDays']):
            month['allDays'][d.date].exclusion.append(d.AMDC.name)
            month['allDays'][d.date-2].exclusion.append(d.AMDC.name)
        elif d.date == 1:
            month['allDays'][d.date].exclusion.append(d.AMDC.name)
        elif d.date == len(month['allDays']):
            month['allDays'][d.date-2].exclusion.append(d.AMDC.name)

        d.AMDC.points_earned_this_month += 1
        d.AMDC.NoOfWkeds_done_this_month += 0.5
        d.PMDC.shifts_this_month += 1
        d.PMDC.AMdates_served.append(d.date)

        month['totalPoints'] += 1
        month['totalNumberOfWeekends'] += 0.5

def PMWDselection():
    month['PMWeekdayShifts'].sort(key = lambda day:len(day.exclusion))
    for d in month['PMWeekdayShifts']:
        d.PMavailable = NSF.night.copy()
        for boi in d.PMavailable:
            for name in d.exclusion:
                if boi.name == name:
                    d.PMavailble.remove(boi)
        d.PMavailable.sort(key = lambda boi:boi.points)
        d.PMDC = d.PMavailable[0]
        d.PMavailable.remove(d.PMDC)
        d.PMDC.points += 0.5

        if d.date != 1 or d.date != len(month['allDays']):
            month['allDays'][d.date].exclusion.append(d.PMDC.name)
            month['allDays'][d.date-2].exclusion.append(d.PMDC.name)
        elif d.date == 1:
            month['allDays'][d.date].exclusion.append(d.PMDC.name)
        elif d.date == len(month['allDays']):
            month['allDays'][d.date-2].exclusion.append(d.PMDC.name)


        d.PMDC.points_earned_this_month += 0.5
        d.PMDC.shifts_this_month += 1
        d.PMDC.PMdates_served.append(d.date)

        month['totalPoints'] += 0.5

def AMWDselection():
    month['AMWeekdayShifts'].sort(key = lambda day:len(day.exclusion))
    for d in month['AMWeekdayShifts']:
        d.available = NSF.all.copy()
        for boi in d.available:
            for name in d.exclusion:
                if boi.name == name:
                    d.availble.remove(boi)
        d.available.sort(key = lambda boi:boi.points)
        d.AMDC = d.available[0]
        d.available.remove(d.AMDC)
        d.AMDC.points += 0.5

        if d.date != 1 or d.date != len(month['allDays']):
            month['allDays'][d.date].exclusion.append(d.AMDC.name)
            month['allDays'][d.date-2].exclusion.append(d.AMDC.name)
        elif d.date == 1:
            month['allDays'][d.date].exclusion.append(d.AMDC.name)
        elif d.date == len(month['allDays']):
            month['allDays'][d.date-2].exclusion.append(d.AMDC.name)

        d.PMDC.points_earned_this_month += 0.5
        d.PMDC.shifts_this_month += 1
        d.PMDC.AMdates_served.append(d.date)

        month['totalPoints'] += 0.5


def setDuty(name:str, when:int, shift:str):
    for nsf in NSF.all:
        if nsf.name == name:
            boi = nsf
    
    #when is the date as an integer
    d = month['allDays'][when]

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

    if shiftType == 0 or shiftType == 2:
        d.AMDC = boi
        boi.AMdates_served.append(d.date)

        if d in month['AMWeekdayShifts']:
            month['AMWeekdayShifts'].remove(d)
            boi.points += 0.5
            boi.points_earned_this_month += 0.5
        elif d in month['AMWeekendShifts']:
            month['AMWeekendShifts'].remove(d)
            boi.points += 1
            boi.NoOfWkeds += 0.5
            boi.points_earned_this_month += 1
            
            
    if shiftType == 0 or shiftType == 1:
        d.PMDC = boi
        boi.PMdates_served.append(d.date)

        if d in month['PMWeekdayShifts']:
            month['PMWeekdayShifts'].remove(d)
            boi.points += 0.5
            boi.points_earned_this_month += 0.5
                
        elif d in month['PMWeekendShifts']:
            month['PMWeekendShifts'].remove(d)
            boi.points += 1
            boi.NoOfWkeds += 0.5
            boi.points_earned_this_month += 1
    
    if shiftType == 0:
        d.AMDC.AMdates_served.remove(d.date)
        d.AMDC.PMdates_served.remove(d.date)
        d.fulldates_served.append(d.date)
            
def setExtra(name:str, when:int, shift:str):
    for nsf in NSF.all:
        if nsf.name == name:
            boi = nsf
    
    #when is the date as an integer
    if when < len(month['allDays']):
        d = month['allDays'][when]
    else:
        raise Exception("date note valid for set date")

    if shift == 'full' and boi.NightDuty == True:
        shiftType = 0
    elif shift == 'pm' and boi.NightDuty == True:
        shiftType = 1
    elif shift == 'am':
        shiftType = 2
    else:
        raise Exception("set duty shift type is wrong")

    d.available.remove(boi)
    if d.date != 1 or d.date != len(month['allDays']):
            month['allDays'][d.date].exclusion.append(d.AMDC.name)
            month['allDays'][d.date-2].exclusion.append(d.AMDC.name)
    elif d.date == 1:
        month['allDays'][d.date].exclusion.append(d.AMDC.name)
    elif d.date == len(month['allDays']):
         month['allDays'][d.date-2].exclusion.append(d.AMDC.name)

    if shiftType == 0 or shiftType == 2:
        d.AMDC = boi
        boi.AMdates_served.append(d.date)
        boi.shifts_this_month += 1 
        if d in month['AMWeekdayShifts']:
            month['AMWeekdayShifts'].remove(d)
        elif d in month['AMWeekendShifts']:
            month['AMWeekendShifts'].remove(d)
            
    if shiftType == 0 or shiftType == 1:
        d.PMDC = boi
        boi.PMdates_served.append(d.date)
        boi.shifts_this_month += 1
        if d in month['PMWeekdayShifts']:
            month['PMWeekdayShifts'].remove(d)
                
        elif d in month['PMWeekendShifts']:
            month['PMWeekendShifts'].remove(d)


    


def updateMonth():
    month['averagePoints'] = month['totalPoints']/len(NSF.all)
    month['averageNumberOfWeekends'] = month['totalNumberOfWeekends']/len(NSF.all)
    month['totalShifts'] = month['totalDays']*2
    month['averageShifts'] = round(month['totalShifts']/len(NSF.all))


    for boi in NSF.all:
        boi.points -= month['averagePoints']
        boi.NoOfNoOfWkeds -= month['averageNumberOfWeekends']


        


def DCselection():
    PMWEselection()
    AMWEselection()
    PMWDselection()
    AMWDselection()


def fullDayPreferance():
    for boi in NSF.morning:
        AMwkeds = month['AMWeekendShifts'].copy()
        NSF.all.sort(key = lambda boi:boi.NoOfWkeds)
        while NSF.all.index(boi) < len(AMwkeds):
            for d in boi.exclusionDays:
                for e in AMwkeds:
                    if e.date == d:
                        AMwkeds.remove(e)
            if len(AMwkeds) == 0:
                break
            AMwkeds.sort(key = lambda day:len(day.exclusion), reverse = True)

            AMwkeds[0].AMDC = boi
            AMwkeds[0].available.remove(boi)
            AMwkeds[0].AMDC.NoOfWkeds += 0.5
            AMwkeds[0].AMDC.points += 1

            NSF.night.sort(key = lambda boi:boi.NoOfWkeds)
            AMwkeds[0].PMDC = NSF.night[0]
            AMwkeds[0].available.remove(NSF.night[0])
            AMwkeds[0].PMDC.NoOfWkeds += 0.5
            AMwkeds[0].PMDC.points += 1

            AMwkeds.remove(AMwkeds[0])
            month['AMWeekendShifts'].remove(AMwkeds[0])

            NSF.all.sort(key = lambda boi:boi.NoOfWkeds)
            AMwkeds.sort(key = lambda day:len(day.exclusion), reverse = True)



def alert():
    i = 0
    while i < month['totalDays']:
        if month['allDays'][i].AMDC == month['allDays'][i].PMDC and month['allDays'][i].AMDC == month['allDays'][i+1].AMDC:
            print(month['allDays'][i].AMDC.name + ',' + month['allDays'][i].date + ',' + month['allDays'][i+1].date)

        
        elif month['allDays'][i].PMDC == month['allDays'][i+1].AMDC and month['allDays'][i].PMDC == month['allDays'][i+1].PMDC:
            print(month['allDays'][i].AMDC.name + ',' + month['allDays'][i].date + ',' + month['allDays'][i+1].date)
        i+=1


def reserveSelection():
    for d in month['allDays']:
        AMbr = d.AMDC.__class__.name
        if AMbr == 'S1':
            d.AMreserveList = S1.all.copy()
        elif AMbr == 'S2':
            d.AMreserveList = S2.all.copy()
        elif AMbr == 'S3':
            d.AMreserveList = S3.all.copy()
        elif AMbr == 'S4':
            d.AMreserveList = S4.all.copy()
        elif AMbr == 'HQCOY':
            d.AMreserveList = HQCOY.all.copy()

        d.AMreserveList.remove(d.AMDC)

        for boi in d.AMreserveList:
            for dood in d.exclusion:
                if boi == dood:
                    d.AMreserveList.remove(boi)
        if d.AMreserveList != []:
            d.AMreserve = random.choice(d.AMreserveList)
        else:
            d.AMreserve = random.choice(d.available)
        
        PMbr = d.PMDC.__class__.name
        if PMbr == 'S1':
            d.PMreserveList = S1.night.copy()
        elif PMbr == 'S2':
            d.PMreserveList = S2.night.copy()
        elif PMbr == 'S3':
            d.PMreserveList = S3.night.copy()
        elif PMbr == 'S4':
            d.PMreserveList = S4.night.copy()
        elif PMbr == 'HQCOY':
            d.PMreserveList = HQCOY.night.copy()

        d.PMreserveList.remove(d.PMDC)

        for boi in d.PMreserveList:
            for dood in d.exclusion:
                if boi == dood:
                    d.PMreserveList.remove(boi)
        if d.PMreserveList != []:
            d.PMreserve = random.choice(d.PMreserveList)
        else:
            d.PMreserve = random.choice(d.PMavailable)


def initNSF():
    with open('NSF.csv', 'r') as NSF_file:
        NSF_reader = csv.reader(NSF_file)

        for line in NSF_reader:
            if line[0] == '*':
                if line[1] == 'S1':
                    S1(line[2], line[3], line[8], line[9])
                elif line[1] == 'S2':
                    S2(line[2], line[3], line[8], line[9])
                elif line[1] == 'S3':
                    S3(line[2], line[3], line[8], line[9])
                elif line[1] == 'S4':
                    S4(line[2], line[3], line[8], line[9])
                elif line[1] == 'HQCOY':
                    HQCOY(line[2], line[3], line[8], line[9])
            else:
                next(NSF_reader)
        

                

def updateCommitment():
    with open('commitment.csv') as commitment_file:
        commitment_reader = csv.reader(commitment_file)

        next(commitment_reader)

        for line in commitment_reader:
            for boi in NSF.all:
                if line[0] == boi.name:
                    listOfDays = line[1].split('/')
                    for e in listOfDays:
                        if '-' in e:
                            e.split('-')
                            i = int(e[0])
                            o = int(e[1])
                            while i <= o:
                                boi.exclusionDays.append(i)
                                i += 1
                        else:
                            boi.exclusionDays.append(int(e))



def printPoints():
    with open('points.csv') as points_file:
        points_writer = csv.writer(points_file)

        points_writer.writerow('branch, name, nightduty, points from last month, no. of wkends last month, points earned this month, no. of wkends this month, total points, total no. of wkends')

        points_writer.writerow(" ")
        points_writer.writerow(f"Average points: {month['averagePoints']}")
        points_writer.writerow(f"Average wkeds: {month['averageNumberOfWeekends']}")

        points_writer.writerow(" ")
        points_writer.writerow(" ")
        points_writer.writerow("S1 Branch:")
        for boi in S1.all:
            br = boi.__class__.name
            points_writer.writerow("*",br, boi.name, boi.NightDuty, boi.points_from_last_month, boi.NoOfWkeds_from_last_month, boi.points_earned_this_month, boi.NoOfWkeds_done_this_month, boi.points, boi.NoOfWkeds)

        points_writer.writerow(" ")
        points_writer.writerow(" ")
        points_writer.writerow("S2 Branch:")
        for boi in S2.all:
            br = boi.__class__.name
            points_writer.writerow("*",br, boi.name, boi.NightDuty, boi.points_from_last_month, boi.NoOfWkeds_from_last_month, boi.points_earned_this_month, boi.NoOfWkeds_done_this_month, boi.points, boi.NoOfWkeds)

        points_writer.writerow(" ")
        points_writer.writerow(" ")
        points_writer.writerow("S3 Branch:")
        for boi in S3.all:
            br = boi.__class__.name
            points_writer.writerow("*",br, boi.name, boi.NightDuty, boi.points_from_last_month, boi.NoOfWkeds_from_last_month, boi.points_earned_this_month, boi.NoOfWkeds_done_this_month, boi.points, boi.NoOfWkeds)

        points_writer.writerow(" ")
        points_writer.writerow(" ")
        points_writer.writerow("S4 Branch:")
        for boi in S4.all:
            br = boi.__class__.name
            points_writer.writerow("*",br, boi.name, boi.NightDuty, boi.points_from_last_month, boi.NoOfWkeds_from_last_month, boi.points_earned_this_month, boi.NoOfWkeds_done_this_month, boi.points, boi.NoOfWkeds)

       
        points_writer.writerow(" ")
        points_writer.writerow(" ")
        points_writer.writerow("HQCOY Branch:")
        for boi in HQCOY.all:
            br = boi.__class__.name
            points_writer.writerow("*",br, boi.name, boi.NightDuty, boi.points_from_last_month, boi.NoOfWkeds_from_last_month, boi.points_earned_this_month, boi.NoOfWkeds_done_this_month, boi.points, boi.NoOfWkeds)


def printDates():
    with open('dates.csv') as dates_file:
        dates_writer = csv.writer(dates_file)

        dates_writer.writerow('name, AM_Shifts_Dates, PM_Shift_dates, Full_Shift_dates, reserve_dates')
        dates_writer.writerow(f"Average shifts: {month['averageShifts']}")

        dates_writer.writerow(" ")
        dates_writer.writerow(" ")
        dates_writer.writerow("S1 Branch:")
        for boi in S1.all:
            dates_writer.writerow(boi.name, boi.AMdates_served, boi.PMdates_served, boi.fulldates_served, boi.reservedates)

        dates_writer.writerow(" ")
        dates_writer.writerow(" ")
        dates_writer.writerow("S2 Branch:")
        for boi in S2.all:
            dates_writer.writerow(boi.name, boi.AMdates_served, boi.PMdates_served, boi.fulldates_served, boi.reservedates)
        
        dates_writer.writerow(" ")
        dates_writer.writerow(" ")
        dates_writer.writerow("S3 Branch:")
        for boi in S3.all:
            dates_writer.writerow(boi.name, boi.AMdates_served, boi.PMdates_served, boi.fulldates_served, boi.reservedates)
        
        dates_writer.writerow(" ")
        dates_writer.writerow(" ")
        dates_writer.writerow("S4 Branch:")
        for boi in S4.all:
            dates_writer.writerow(boi.name, boi.AMdates_served, boi.PMdates_served, boi.fulldates_served, boi.reservedates)
        
        dates_writer.writerow(" ")
        dates_writer.writerow(" ")
        dates_writer.writerow("HQCOY Branch:")
        for boi in HQCOY.all:
            dates_writer.writerow(boi.name, boi.AMdates_served, boi.PMdates_served, boi.fulldates_served, boi.reservedates)


def printRoster():
    with open('roster.csv') as roster_file:
        roster_writer = csv.writer(roster_file)

        for day in month['allDays']:
            roster_writer.writerow(f'{day.date} AM: ')
            roster_writer.writerow(f'main: {day.AMDC.name}')
            roster_writer.writerow(f'reserve: {day.AMreserve}')
            roster_writer.writerow(" ")
            roster_writer.writerow(f'{day.date} PM: ')
            roster_writer.writerow(f'main: {day.PMDC.name}')
            roster_writer.writerow(f'reserve: {day.PMreserve}')
            roster_writer.writerow(" ")
            roster_writer.writerow(" ")

def generateCompleteRoster(monthDate:int, year:int, totalDays:int, firstDay:str):
    mD = monthDate
    y = year
    tD = totalDays
    fD = firstDay
    generateMonth(mD, y, tD, fD)

    initNSF()
    updateCommitment()

    updateExclusion()

    #setDuty()
    #setExtra()

    DCselection()

    alert()

    reserveSelection()

    updateMonth()

    printPoints()
    printDates()
    printRoster()

generateCompleteRoster(12, 2021, 31, "Wednesday")
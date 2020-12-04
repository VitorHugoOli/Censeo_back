from datetime import date, timedelta

choseDay = 2
sdate = date(2020, 8, 13)  # start date//Qua
edate = date(2020, 10, 15)  # end date//ter

daysToNumberVar = {"seg": 0,
                   "ter": 1,
                   "qua": 2,
                   "qui": 3,
                   "sex": 4,
                   "sab": 5,
                   "dom": 6}


def dayToNumber(day):
    try:
        day = int(day)
        if 0 <= (day - 1) <= 6:
            return day - 1
        else:
            return -1
    except ValueError as ex:
        return daysToNumberVar[day.lower()] if day.lower() in daysToNumberVar else -1
    except:
        return -1


def amountDayBetweenTwoDates(sdate, edate, chose_day):
    '''
    this Algorithm is O(1)
    :param sdate: 
    :param edate: 
    :param chose_day: 
    :return: the total of the chose_day between two dates
    '''
    monday1 = (sdate - timedelta(days=sdate.weekday()))
    monday2 = (edate - timedelta(days=edate.weekday()))  # Desconsidera a ultima semana
    semanas = ((monday2 - monday1).days / 7) - 1  # The mines one refers to the first week
    countWeek = semanas
    if sdate.weekday() <= chose_day:
        countWeek += 1
    if edate.weekday() >= chose_day:
        countWeek += 1
    return countWeek


def amountDayBetweenTwoDates2(sdate, edate, chose_day):
    '''
    this Algorithm is O(n) 
    :param sdate: 
    :param edate: 
    :param chose_day: 
    :return: the total of the chose_day between two dates
    '''
    delta = edate - sdate  # as timedelta
    countWeek = 0
    for i in range(0, delta.days + 1, 1):
        day = sdate + timedelta(days=i)
        if day.weekday() == 2:
            countWeek += 1
        print(day.strftime("%a") + " - " + day.weekday().__str__())
    return countWeek


'''

Mon - 0
Tue - 1
Wed - 2
Thu - 3
Fri - 4
Sat - 5
Sun - 6

'''

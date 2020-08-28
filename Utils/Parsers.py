daysToNumberVar = {"seg": 1,
                   "ter": 2,
                   "qua": 3,
                   "qui": 4,
                   "sex": 5,
                   "sab": 6,
                   "dom": 7}


def dayToEnum(day: str):
    '''
    This function convert any string of a day in a number that is related with the enum of days in the BD
    :param day:
    :return:
    '''
    dia = day[0:3].lower()
    return daysToNumberVar[dia]

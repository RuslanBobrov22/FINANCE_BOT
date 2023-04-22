import datetime

# коннект к времени


def data_get():
    d = str(datetime.date.today()).split('-')
    return d[1] + d[2]
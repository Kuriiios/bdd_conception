import datetime
from random import randrange

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)

d = datetime.datetime.now().date()
d_plus_two_w = d.replace(day=d.day + 14)
d_plus_five_y = d.replace(year=d.year + 5)
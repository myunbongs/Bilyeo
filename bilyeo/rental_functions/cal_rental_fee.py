import datetime
from bilyeo.models import Stuff


def find_total_rental_fee(rental_date, return_date, pk):
    days = rental_date - return_date
    stuff = Stuff.objects.get(pk=pk)
    total = abs(days.days * stuff.fee)
    return total
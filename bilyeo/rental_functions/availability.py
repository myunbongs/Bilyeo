import datetime
from bilyeo.models import Stuff, Rental

def check_availability(stuff, rental_date, return_date):
    available_list = []
    rental_list =  Rental.objects.filter(stuff=stuff)
    for rental in rental_list:
        if rental.rental_date > return_date or rental.return_date < rental_date:
            available_list.append(True)
        else:
            available_list.append(False)
    return all(available_list)

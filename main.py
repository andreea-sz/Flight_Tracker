#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
import time
import datetime

DEPARTURE_CITY = 'LON'



sheet = DataManager()
sheet_data = sheet.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

for item in sheet_data:
    if not item["iataCode"]:
        code = flight_search.get_destination_code(item['city'])
        item["iataCode"] = code
        time.sleep(2)


sheet.destination_data = sheet_data
sheet.update_destination_codes()

start_date = datetime.datetime.now() + datetime.timedelta(days=1)
return_date = start_date + datetime.timedelta(days=(8))


for destination_city in sheet_data:
    flights = flight_search.get_flights(DEPARTURE_CITY, destination_city["iataCode"], start_date, return_date)
    print(f"Getting Flights to {destination_city['city']}...")
    cheapest_price = find_cheapest_flight(flights)
    if cheapest_price.price != "N/A" and cheapest_price.price < destination_city["lowestPrice"]:
        print(f"We found a cheaper flight for {destination_city['city']}: €{cheapest_price.price}")
        message = f'Travel to {destination_city["city"]} lower price alert! Only €{cheapest_price.price} ' \
                  f'to fly from {cheapest_price.departure_airport} to {cheapest_price.arrival_airport} ' \
                  f'on {cheapest_price.outbound_date} until {cheapest_price.inbound_date}'
        notification_manager.send_message(message)



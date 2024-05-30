

class FlightData:
    def __init__(self, price, departure_airport, arrival_airport, outbound_date, inbound_date):
        self.price = price
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date


def find_cheapest_flight(flights):
    if flights is None or not flights['data']:
        return FlightData("N/A","N/A","N/A","N/A","N/A")

    min_price = ""
    item_info = {}
    for item in flights["data"]:
        if not min_price:
            min_price = item['price']['total']
            item_info = item["itineraries"]
        elif min_price > item['price']['total']:
            min_price = item['price']['total']
            item_info = item["itineraries"]

    price = float(min_price)
    departure_airport = item_info[0]["segments"][0]["departure"]["iataCode"]
    arrival_airport = item_info[0]["segments"][0]["arrival"]["iataCode"]
    outbound_date = item_info[0]["segments"][0]["departure"]["at"].split("T")[0]
    inbound_date = item_info[1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(price, departure_airport, arrival_airport, outbound_date, inbound_date)

    return cheapest_flight



import requests
import os
import datetime

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
CITY_CODE_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"



class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.api_key = os.environ["FLIGHT_API_KEY"]
        self.api_pass = os.environ["FLIGHT_API_PASS"]
        self.token = self.get_token()

    def get_token(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        token_params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_pass,
        }

        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=token_params)
        token_data = response.json()

        return token_data['access_token']


    def get_destination_code(self, city):
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        query = {
            "subType": "CITY",
            "keyword": city,
        }
        response = requests.get(url=CITY_CODE_ENDPOINT, headers=header, params=query)
        try:
            iata_code = response.json()['data'][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city}.")
            return "Not Found"

        return iata_code

    def get_flights(self,departure_IATA, destination_IATA, from_time, to_time):

        header = {
            "Authorization": f"Bearer {self.token}"
        }

        query = {
            "originLocationCode": departure_IATA,
            "destinationLocationCode": destination_IATA,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": '1',
            "nonStop": "true",
            "currencyCode": "EUR",
            "max": "10"
        }

        response = requests.get(url=FLIGHT_ENDPOINT, headers=header, params=query)

        if response.status_code != 200:
            print(f"Check Flights response code : {response.status_code}")
            print(f"There was an error with the flight search\nResponse code: {response.text}")
            return None

        return response.json()

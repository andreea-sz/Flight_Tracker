import requests
import os

SHEETY_API_ENDPOINT = os.environ["SHEETY_ENDPOINT"]


class DataManager:
    def __init__(self):
        self.token = os.environ["SHEETY_TOKEN"]
        self.sheety_authentication = {
            "Authorization": f"Basic {self.token}"
        }
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_API_ENDPOINT, headers=self.sheety_authentication)
        data = response.json()
        print(data)
        self.destination_data = data["prices"]

        return self.destination_data

    def update_destination_codes(self):
        for item in self.destination_data:
            param_to_edit = {
                "price": {
                    "iataCode" : item["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_API_ENDPOINT}/{item['id']}",
                                    headers=self.sheety_authentication, json=param_to_edit)


            print(response.text)


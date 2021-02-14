import requests
from json import loads
from settings import TP_URL, ACCESS_TOKEN

class Creater():
    def __init__(self, entity_type, data = None):
        self.request_url = self.set_request_url(entity_type)
        self.data = data

    def set_request_url(self, entity_type):
        return TP_URL + entity_type + "/bulk?include=[ID]&format=json&access_token=" + ACCESS_TOKEN

    def upload_entity(self):
        response = requests.post(self.request_url, json=self.data)
        if(response.status_code == 200):
            id_list = []
            new_entities = response.json()
            for entity in new_entities["Items"]:
                id_list.append(entity["Id"])
            return id_list
        else:
            print("Status Code: ", response.status_code)
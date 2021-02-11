import requests
from json import loads
from settings import TP_URL, ACCESS_TOKEN

class Uploader():
    def __init__(self, entity_type, data = None):
        self.request_url = self.set_request_url(entity_type)
        self.data = data

    def set_request_url(self, entity_type):
        return TP_URL + entity_type + "/bulk?include=[ID]&format=json&access_token=" + ACCESS_TOKEN

    def upload_new_test_cases(self):
        response = requests.post(self.request_url, self.data)
        return response.status_code, loads(response.json())["Items"][0]["Id"]
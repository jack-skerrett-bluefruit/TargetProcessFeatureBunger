import requests
from settings import TP_URL, ACCESS_TOKEN

class Uploader():
    def __init__(self, entity_type, data = None):
        self.request_url = self.set_request_url(entity_type)
        self.data = data

    def set_request_url(self, entity_type):
        return TP_URL + entity_type + "/bulk?include=[ID]&access_token=" + ACCESS_TOKEN

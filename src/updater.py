from settings import TP_URL, ACCESS_TOKEN
import requests

class Updater:
    def __init__(self, feature_name, feature_id, project_id, ):
        self.feature_name = feature_name
        self.feature_id = feature_id
        self.project_id = project_id
        self.check_feature_exists_request_url = self.set_request_url()

    def set_request_url(self):
        return f"{TP_URL}Features?where=(Name eq \'{self.feature_name}\') and (Project.Id eq {self.project_id})&include=[Id]&format=json&access_token={ACCESS_TOKEN}"

    def check_feature(self):
        response = requests.get(self.check_feature_exists_request_url)
        return response.status_code
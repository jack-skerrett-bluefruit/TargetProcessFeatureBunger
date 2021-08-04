from settings import TP_URL, ACCESS_TOKEN
from fetcher import Fetcher
import requests

class Updater:
    def __init__(self, local_tp_feature_file):
        self.feature_name = local_tp_feature_file.feature_name
        self.project_id = local_tp_feature_file.project
        self.local_tp_feature_file = local_tp_feature_file.tp_format_feature_file

    def construct_feature_check_request(self):
        return f"{TP_URL}Features?where=(Name eq \'{self.feature_name}\') and (Project.Id eq {self.project_id})&include=[Id]&format=json&access_token={ACCESS_TOKEN}"

    def does_feature_exist(self):
        request = self.construct_feature_check_request()
        response = requests.get(request)
        if(response.status_code == 200):
            feature = response.json()
            self.remote_feature_id = feature["Items"][0]["Id"]
            return True
        else:
            return False

    def find_tests_that_are_local_and_remote(self):
        fetcher = Fetcher(self.remote_feature_id)
        fetcher.construct_feature_get_request()
        fetcher.get_test_case_ids_for_a_feature()
        self.find_duplicates_in_two_json_features(fetcher.test_case_ids)
        
    def find_duplicates_in_two_json_features(self, remote_feature):
        #need to iterate through two lists and be really smart, I just dont know how
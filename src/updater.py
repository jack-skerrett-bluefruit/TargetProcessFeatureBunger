from settings import TP_URL, ACCESS_TOKEN
import requests

class Updater:
    def __init__(self, feature_name, project_id, feature_file):
        self.feature_name = feature_name
        self.project_id = project_id
        self.check_feature_exists_request_url = self.set_request_url()

    def set_request_url(self):
        return f"{TP_URL}Features?where=(Name eq \'{self.feature_name}\') and (Project.Id eq {self.project_id})&include=[Id]&format=json&access_token={ACCESS_TOKEN}"

    def check_feature(self):
        response = requests.get(self.check_feature_exists_request_url)
        if(response.status_code == 200):
            feature = response.json()
            self.feature_id = feature["Items"][0]["Id"]
            return True
        else:   #I'm unsure about this. I want to look for a 404 to indicate an error, other status codes could mean there is an issue with the API, and the feature DOES exist
            return False

    def set_test_cases_of_an_existing_feature(self):
        existing_feature = self.get_test_cases_of_an_existing_feature()
        self.test_cases = []
        for test_case in existing_feature["LinkedTestPlan"]["TestCases"]["Items"]:
            self.test_cases.append(test_case["Id"])

    def get_test_cases_of_an_existing_feature(self):
        response = requests.get(f"{TP_URL}Features/{self.feature_id}/?format=json&include=[LinkedTestPlan[TestCases[Id]]]&access_token={ACCESS_TOKEN}")
        return response.json()

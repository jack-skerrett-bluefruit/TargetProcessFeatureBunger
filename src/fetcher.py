from settings import TP_URL, ACCESS_TOKEN
import requests
"""
You give fetcher a feature, and it will get all the test cases for said feature
"""

class Fetcher():
    def __init__(self, feature_id):
        self.feature_id = feature_id

    def construct_feature_get_request(self):
        return f"{TP_URL}Features/47536?include=[LinkedTestPlan[TestCases[Id]]]&format=json&access_token={ACCESS_TOKEN}"

    def construct_test_step_get_requests(self):
        self.test_step_requests = []
        for id in self.test_case_ids:
            self.test_step_requests.append(f"{TP_URL}TestCases/{id}?include=[TestSteps[Id]]&format=json&access_token={ACCESS_TOKEN}")

    def get_test_case_ids_for_a_feature(self):
        request = self.construct_feature_get_request()
        response = requests.get(request)
        if(response.status_code == 200):
            self.extract_test_case_ids_from_feature(response.json())
            return True
        else:
            return False

    def extract_test_case_ids_from_feature(self, response_body):
        self.test_case_ids = []
        for test_case in response_body["LinkedTestPlan"]["TestCases"]["Items"]:
            self.test_case_ids.append(int(test_case["Id"]))
        return self.test_case_ids

    def get_tests_from_ids(self):
        self.test_cases = []
        for request in self.test_step_requests:
            response = requests.get(request)
            self.test_cases.append(response.json())

        

from settings import ID_DICT_LIST_ITEM, ASSIGN_TO_TEST_PLANS, TP_URL, ACCESS_TOKEN
from copy import deepcopy
import requests

class Organiser():
    def __init__(self, feature, test_case):
        self.feature = feature
        self.test_case = test_case
        self.data = self.set_data()
        self.request_url = self.set_request_url()

    def set_data(self):
        assign_data = deepcopy(ASSIGN_TO_TEST_PLANS)
        test_case_id_item = deepcopy(ID_DICT_LIST_ITEM)
        test_case_id_item["ID"] = self.feature
        assign_data["TestPlans"]["Items"].append(test_case_id_item)
        return assign_data

    def set_request_url(self):
        return TP_URL + "TestCases/" + str(self.test_case) + "?format=json&access_token=" + ACCESS_TOKEN

    def link_test_case_to_feature(self):
        response = requests.post(self.request_url, data = self.data)
        return response.status_code, response.json()["Id"]
        
 
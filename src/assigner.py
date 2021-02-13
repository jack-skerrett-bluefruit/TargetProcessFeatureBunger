from settings import ID_DICT_LIST_ITEM, ASSIGN_TO_TEST_PLANS, ASSIGN_TO_FEATURE, TP_URL, ACCESS_TOKEN
from copy import deepcopy
import requests

class Assigner():
    def __init__(self, feature=None, test_plan=None, test_case=None):
        self.feature = feature
        self.test_plan = test_plan
        self.test_case = test_case
        self.data = self.set_data()
        self.request_url = self.set_request_url()

    def set_data(self):
        if(self.feature == None):
            assign_data = deepcopy(ASSIGN_TO_TEST_PLANS)
            test_case_id_item = deepcopy(ID_DICT_LIST_ITEM)
            test_case_id_item["ID"] = self.test_plan
            assign_data["TestPlans"]["Items"].append(test_case_id_item)
            return assign_data
        elif(self.test_case == None):
            assign_data = deepcopy(ASSIGN_TO_FEATURE)
            assign_data["LinkedTestPlan"]["Id"] = self.test_plan
            return assign_data

    def set_request_url(self):
        entity = ""
        if(self.feature == None):
            return TP_URL + "TestCases/" + str(self.test_case) + "?format=json&access_token=" + ACCESS_TOKEN
        elif(self.test_case == None):
            return TP_URL + "Feature/" + str(self.feature) + "?include=[Id, LinkedTestPlan]&format=json&access_token=" + ACCESS_TOKEN
        

    def link_test_case_to_test_plan(self):
        response = requests.post(self.request_url, json = self.data)
        return response.status_code, response.json()["Id"]
        
    def link_test_plan_to_feature(self):
        response = requests.post(self.request_url, json = self.data)
        return response.status_code, response.json()["LinkedTestPlan"]["Id"]
 
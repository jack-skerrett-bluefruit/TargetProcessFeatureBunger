from settings import ID_DICT_LIST_ITEM, ASSIGN_TO_TEST_PLANS, ASSIGN_TO_FEATURE, TP_URL, ACCESS_TOKEN
from copy import deepcopy
import requests

class Assigner():
    def __init__(self, feature=None, test_plan=None, test_case=None):
        self.feature = feature
        self.test_plan = test_plan[0]
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
        if(self.feature == None):
            test_case_urls = []
            for item in self.test_case:
                test_case_urls.append(TP_URL + "TestCases/" + str(item) + "?format=json&access_token=" + ACCESS_TOKEN)
            return test_case_urls
        elif(self.test_case == None):
            feature_urls = []
            for item in self.feature:
                feature_urls.append(TP_URL + "Feature/" + str(item) + "?include=[Id,LinkedTestPlan]&format=json&access_token=" + ACCESS_TOKEN)
            return feature_urls

    def link_test_case_to_test_plan(self):
        for url in self.request_url:
            response = requests.post(url, json = self.data)
        return response.status_code
        
    def link_test_plan_to_feature(self):
        for url in self.request_url:
            response = requests.post(url, json = self.data)
        return response.status_code
 
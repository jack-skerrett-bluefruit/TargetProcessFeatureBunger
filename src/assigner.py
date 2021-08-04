from settings import TP_URL, ACCESS_TOKEN
from copy import deepcopy
import requests

"""
You give the assigner a feature and a test plan or a test plan and test case, it will then link them in Target Process
"""

class Assigner:
    def __init__(self, feature=None, test_plan=None, test_case=None):
        self.feature = feature
        self.test_plan = test_plan[0]
        self.test_case = test_case
        self.test_plan_body = {"TestPlans":{"Items":[]}}
        self.feature_body = {"LinkedTestPlan": {"ResourceType": "TestPlan","Id": ""}}
        self.set_data()
        self.request_url = self.set_request_url()

    def set_data(self):
        if(not self.feature):
            test_case_id_item = {"ID":""}
            test_case_id_item["ID"] = self.test_plan
            self.test_plan_body["TestPlans"]["Items"].append(test_case_id_item)
        elif(not self.test_case):
            self.feature_body["LinkedTestPlan"]["Id"] = self.test_plan

    def set_request_url(self):
        if(not self.feature):
            test_case_urls = []
            for item in self.test_case:
                test_case_urls.append(f"{TP_URL}TestCases/{str(item)}?format=json&access_token={ACCESS_TOKEN}")
            return test_case_urls
        elif(not self.test_case):
            feature_urls = []
            for item in self.feature:
                feature_urls.append(f"{TP_URL}Feature/{str(item)}?include=[Id,LinkedTestPlan]&format=json&access_token={ACCESS_TOKEN}")
            return feature_urls

    def link_test_case_to_test_plan(self):
        for url in self.request_url:
            response = requests.post(url, json = self.test_plan_body)
        return response.status_code
        
    def link_test_plan_to_feature(self):
        for url in self.request_url:
            response = requests.post(url, json = self.feature_body)
        return response.status_code
 
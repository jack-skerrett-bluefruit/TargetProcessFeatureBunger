from src.reader import Reader
from copy import deepcopy
import re

"""
The JSONifier takes a Reader object and converts it into a JSON based format so that it can be sent to the Target Process API
"""

class Jsonifier:
    def __init__(self, feature_file: Reader, project):
        self.feature_file = feature_file
        self.project = project
        self.tp_format_feature_file = []
        self.feature_name = ""
        self.new_test_cases = {"Name": "","Project":{"ID": ""}, "TestSteps": {"Items": []}}
        self.default_test_step = {"ResourceType":"TestStep","Description":""}
        self.feature_body = {"Name":"","Project":{"ID":""}}
        self.set_tp_format_feature_file()
        
        
    def set_tp_format_feature_file(self):
        for list_test_case in self.feature_file.feature_file:
            if(type(list_test_case) == str):
                if(list_test_case.split()[0] == "Feature:"):
                    self.feature_name = list_test_case
                    continue
            test_case = deepcopy(self.new_test_cases)
            test_case["Project"]["ID"] = self.project
            for line in list_test_case:
                if(line == ""):
                    pass
                elif(line[0] == "@"):
                    id = re.findall("\d+", line)
                    test_case["ID"] = int(id[0])
                elif(line[:8] == "Scenario"):
                    test_case["Name"] = line
                else:
                    test_step = deepcopy(self.default_test_step)
                    test_step["Description"] = line
                    test_case["TestSteps"]["Items"].append(test_step)
            self.tp_format_feature_file.append(test_case)

    #This is used by creator when you want to create a Feature File or Test Plan that have never previously existed
    def create_new_feature_or_test_plan_body(self):
        self.feature_body["Name"] = self.feature_name
        self.feature_body["Project"]["ID"] = self.project
        bulk_feature_body = []
        bulk_feature_body.append(self.feature_body)
        return bulk_feature_body
from src.reader import Reader
from copy import deepcopy

class Jsonifier:
    def __init__(self, file_name, project):
        self.reader = Reader(file_name)
        self.project = project
        self.tp_format_feature_file = []
        self.feature_name = ""
        self.new_test_cases = {"Name": "","Project":{"ID": ""}, "TestSteps": {"Items": []}}
        self.default_test_step = {"ResourceType":"TestStep","Description":""}
        self.feature_body = {"Name":"","Project":{"ID":""}}
        self.set_tp_format_feature_file()
        

        
    def set_tp_format_feature_file(self):
        for list_test_case in self.reader.feature_file:
            if(type(list_test_case) == str):
                if(list_test_case.split()[0] == "Feature:"):
                    self.feature_name = list_test_case
                    continue
            test_case = deepcopy(self.new_test_cases)
            test_case["Project"]["ID"] = self.project
            for line in list_test_case:
                if(line == ""):
                    pass
                elif(line[:8] == "Scenario"):
                    test_case["Name"] = line
                else:
                    test_step = deepcopy(self.default_test_step)
                    test_step["Description"] = line
                    test_case["TestSteps"]["Items"].append(test_step)
            self.tp_format_feature_file.append(test_case)

    def create_new_feature_or_test_plan_body(self):
        self.feature_body["Name"] = self.feature_name
        self.feature_body["Project"]["ID"] = self.project
        bulk_feature_body= []
        bulk_feature_body.append(self.feature_body)
        return bulk_feature_body
from src.feature_file_reader import Reader
from settings import NEW_TEST_CASES, DEFAULT_TEST_STEP
from copy import deepcopy

class Jsonifier():
    def __init__(self, file_name, project):
        self.reader = Reader(file_name)
        self.project = project
        self.tp_format_feature_file = []
        self.set_tp_format_feature_file()

        
    def set_tp_format_feature_file(self):
        for list_test_case in self.reader.feature_file:
            test_case = deepcopy(NEW_TEST_CASES)
            test_case["Project"]["ID"] = self.project
            for line in list_test_case:
                if(line == ""):
                    pass
                elif(line[:8] == "Scenario"):
                    test_case["Name"] = line
                else:
                    test_step = deepcopy(DEFAULT_TEST_STEP)
                    test_step["Description"] = line
                    test_case["TestSteps"]["Items"].append(test_step)
            self.tp_format_feature_file.append(test_case)

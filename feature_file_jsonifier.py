from feature_file_reader import Reader
from settings import TP_DICT, DEFAULT_TEST_STEP

class Jsonifier():
    def __init__(self, file_name):
        self.reader = Reader(file_name)
        self.dictionary_feature_file = {}
        
    def set_dictionary_feature_file(self):
        test_case = TP_DICT
        for line in self.reader.feature_file:
            line.strip()
            if(line == ""):
                pass
            elif(line[:8] == "Scenario"):
                test_case["Name"] = line
            else:
                test_step = {"ResourceType":"TestStep","Description":""}
                test_step["Description"] = line
                test_case["TestSteps"]["Items"].append(test_step)
        self.dictionary_feature_file = test_case

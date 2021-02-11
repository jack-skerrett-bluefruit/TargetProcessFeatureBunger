class Reader():
    def __init__(self, file_name):
        self.file_name = file_name
        self.feature_file = []
        self.set_feature_file()

    def set_feature_file(self):
        with open(self.file_name, "r") as f:
            test_case = []
            first_pass = True
            for line in f:
                if(line.strip() == ""):
                    continue
                elif(line[:8] == "Scenario" and not first_pass):
                    self.feature_file.append(test_case)
                    test_case = []
                first_pass = False
                test_case.append(line.strip())
        self.feature_file.append(test_case)
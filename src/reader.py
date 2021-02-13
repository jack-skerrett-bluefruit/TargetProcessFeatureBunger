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
                elif(line.split()[0] == "Feature:"):
                    self.feature_file.append(line.strip())
                elif(line[:8] == "Scenario" and first_pass):
                    test_case.append(line.strip())
                    first_pass = False
                elif(line[:8] == "Scenario" and not first_pass):
                    self.feature_file.append(test_case)
                    test_case = []
                    test_case.append(line.strip())
                elif(line.split()[0] in ("Given", "When", "Then", "And", "But", "Examples:")):
                    test_case.append(line.strip())
                    first_pass = False
                elif("|" in line):
                    test_case.append(line.strip())
                    first_pass = False
        self.feature_file.append(test_case)
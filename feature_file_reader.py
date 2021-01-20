class Reader():
    def __init__(self, file_name):
        self.file_name = file_name
        self.feature_file = []

    def set_feature_file(self):
        with open(self.file_name, "r") as f:
            self.feature_file = f.read().splitlines()

reader = Reader("tests/tests.feature")
reader.set_feature_file()
for line in reader.feature_file:
    print(line)

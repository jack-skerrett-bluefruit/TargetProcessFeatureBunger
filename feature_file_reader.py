class Reader():
    def __init__(self, file_name):
        self.file_name = file_name
        self.feature_file = []

    def set_feature_file(self):
        with open(self.file_name, "r") as f:
            self.feature_file = f.read().splitlines()
        self.format_examples()

    def format_examples(self):
        i = -1
        for line in self.feature_file:
            if(line == "Examples:"):
                self.feature_file.pop(i)
            i += 1


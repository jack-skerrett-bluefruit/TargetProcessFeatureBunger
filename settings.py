from collections import defaultdict

#target process dictionary object

test = defaultdict(list)
test["Name"] = ""
test["TestSteps"] = {"Items":[]}

TP_DICT = test

DEFAULT_TEST_STEP = {"ResourceType":"TestStep","Description":""}
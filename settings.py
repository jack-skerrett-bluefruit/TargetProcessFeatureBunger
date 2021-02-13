from collections import defaultdict

#target process dictionary object

NEW_TEST_CASES = {"Name": "","Project":{"ID": ""}, "TestSteps": {"Items": []}}
DEFAULT_TEST_STEP = {"ResourceType":"TestStep","Description":""}
ASSIGN_TO_TEST_PLANS = {"TestPlans":{"Items":[]}}
ASSIGN_TO_FEATURE = {"LinkedTestPlan": {"ResourceType": "TestPlan","Id": ""}}
ID_DICT_LIST_ITEM = {"ID": ""}
CREATE_FEATURE_OR_TEST_PLAN_BODY = {"Name":"","Project":{"ID":""}}


#TP
TP_URL = "https://bluefruit.tpondemand.com/api/v1/"
ACCESS_TOKEN = "testaccesstoken"
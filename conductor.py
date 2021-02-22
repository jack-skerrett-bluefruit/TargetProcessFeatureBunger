from src.jsonifier import Jsonifier
from src.creater import Creater
from src.assigner import Assigner

j = Jsonifier("tests/whole_feature.feature", 29234)
c1 = Creater("Features", j.create_new_feature_or_test_plan_body())
c2 = Creater("TestPlans", j.create_new_feature_or_test_plan_body())
c3 = Creater("TestCases", j.tp_format_feature_file)

feature_id = c1.upload_entity()
plan_id = c2.upload_entity()
test_case_id = c3.upload_entity()

a1 = Assigner(feature = feature_id, test_plan = plan_id)
a2 = Assigner(test_plan = plan_id, test_case = test_case_id)

a2.link_test_case_to_test_plan()
a1.link_test_plan_to_feature()
from unittest import mock
from src.assigner import Assigner
from pytest import fixture

@fixture
def assign_test_case_to_plan():
    return Assigner(test_plan=[54321], test_case=[12345])

@fixture
def assign_multiple_test_cases_to_plan():
    return Assigner(test_plan=[54321], test_case=[12345,12346,12347,12348])

@fixture
def assign_test_plan_to_feature():
    return Assigner(feature=[99999], test_plan=[54321])

def test_feature_assigner_initialises_withtest_case_id_and_test_plan_id_to_assign_it_to():
    assigner = Assigner(feature=[99999], test_plan=[54321], test_case=[12345])
    assert assigner.feature == [99999]
    assert assigner.test_plan == 54321
    assert assigner.test_case == [12345]

def test_assigner_constructs_correct_data_for_assinging_a_test_case_to_a_test_plan(assign_test_case_to_plan):
    expected_data = {
        "TestPlans":{
            "Items":[
                {"ID": 54321}
                ]
            }
        }
    assert assign_test_case_to_plan.test_plan_body == expected_data

def test_assigner_creates_the_correct_url_to_post_test_case_assignment_to(assign_test_case_to_plan):
    expected_url = ["https://bluefruit.tpondemand.com/api/v1/TestCases/12345?format=json&access_token=testaccesstoken"]
    assert assign_test_case_to_plan.request_url == expected_url

@mock.patch("src.assigner.requests.post")
def test_test_case_is_linked_to_test_plan(mock_request_post, assign_test_case_to_plan):
    mock_request_post.return_value = mock.Mock(name="mock_api_response",
                                                **{"status_code": 200, "json.return_value": {"ResourceType": "TestCase","Id": 12345}})
    assert assign_test_case_to_plan.link_test_case_to_test_plan() == 200
 
def test_assigner_constructs_correct_data_for_assinging_a_test_plan_to_a_feature(assign_test_plan_to_feature):
    expected_data = {
        "LinkedTestPlan": {
            "ResourceType": "TestPlan",
            "Id": 54321
            }
    }
    assert assign_test_plan_to_feature.feature_body == expected_data

def test_assigner_creates_the_correct_url_to_post_test_plan_assignment_to(assign_test_plan_to_feature):
    expected_url = ["https://bluefruit.tpondemand.com/api/v1/Feature/99999?include=[Id,LinkedTestPlan]&format=json&access_token=testaccesstoken"]
    assert assign_test_plan_to_feature.request_url == expected_url


@mock.patch("src.assigner.requests.post")
def test_test_plan_is_linked_to_feature(mock_request_post, assign_test_plan_to_feature):
    mock_request_post.return_value = mock.Mock(name="mock_api_response",
                                                **{"status_code": 200, "json.return_value": {"ResourceType": "Feature","Id": 99999,"LinkedTestPlan": {"ResourceType": "TestPlan","Id": 54321,"Name": "Feature: Whole Feature"}}})
    assert assign_test_plan_to_feature.link_test_plan_to_feature() ==  200

def test_assigner_stores_multiple_test_case_ids_as_a_list(assign_multiple_test_cases_to_plan):
    assert type(assign_multiple_test_cases_to_plan.test_case) == list
    assert assign_multiple_test_cases_to_plan.test_case == [12345,12346,12347,12348]

def test_assigner_creates_multiple_request_url_when_given_multiple_test_case_ids(assign_multiple_test_cases_to_plan):
    expected_urls = ["https://bluefruit.tpondemand.com/api/v1/TestCases/12345?format=json&access_token=testaccesstoken",
            "https://bluefruit.tpondemand.com/api/v1/TestCases/12346?format=json&access_token=testaccesstoken",
            "https://bluefruit.tpondemand.com/api/v1/TestCases/12347?format=json&access_token=testaccesstoken",
            "https://bluefruit.tpondemand.com/api/v1/TestCases/12348?format=json&access_token=testaccesstoken"]
    
    assert assign_multiple_test_cases_to_plan.request_url == expected_urls 
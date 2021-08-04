from pytest import fixture
from src.fetcher import Fetcher
import requests

class GetFeatureIdsSuccessResponse:
    status_code = 200

    @staticmethod
    def json():
        return {
            "ResourceType": "Feature",
            "Id": 47536,
            "LinkedTestPlan": {
                "ResourceType": "TestPlan",
                "Id": 47537,
                "TestCases": {
                    "Items": [
                        {"ResourceType": "TestCase","Id": 47543},
                        {"ResourceType": "TestCase","Id": 47544},
                        {"ResourceType": "TestCase","Id": 47538}
                    ]}}}

#class GetFeatureIdsFailureResponse:
#    status_code = 400

class GetTestStepsSuccessResponse():
    status_code = 200

    @staticmethod
    def json():
        return {
    "ResourceType": "TestCase",
    "Id": 34566,
    "Name": "Scenario: This is a test title",
    "TestSteps": {
        "Items": [
            {
                "ResourceType": "TestStep",
                "Id": 77777,
            },
            {
                "ResourceType": "TestStep",
                "Id": 77778,
            },
            {
                "ResourceType": "TestStep",
                "Id": 77779,
            }
        ]
    }
}

        
@fixture
def fetcher():
    return Fetcher(99999)

def test_that_fetcher_initilises_with_a_feature_id(fetcher):
    assert fetcher.feature_id == 99999

def test_that_fetcher_constructs_a_request_for_getting_all_test_case_ids_associated_with_the_linked_test_plan_of_a_feature(fetcher):
    assert fetcher.construct_feature_get_request() == "https://bluefruit.tpondemand.com/api/v1/Features/47536?include=[LinkedTestPlan[TestCases[Id]]]&format=json&access_token=testaccesstoken"

def test_that_fetcher_extracts_test_cases_from_a_feature_response(fetcher, monkeypatch):
    def mock_get(*args, **kwargs):
        return GetFeatureIdsSuccessResponse()
    monkeypatch.setattr(requests, "get", mock_get)

    fetcher.get_test_case_ids_for_a_feature()
    assert fetcher.test_case_ids == [47543, 47544, 47538]

def test_that_fetcher_constructs_requests_for_getting_test_steps_of_given_test_cases(fetcher, monkeypatch):
    fetcher.test_case_ids = [47543, 47544, 47538]
    fetcher.construct_test_step_get_requests()
    assert fetcher.test_step_requests == [
        "https://bluefruit.tpondemand.com/api/v1/TestCases/47543?include=[TestSteps[Id]]&format=json&access_token=testaccesstoken",
        "https://bluefruit.tpondemand.com/api/v1/TestCases/47544?include=[TestSteps[Id]]&format=json&access_token=testaccesstoken",
        "https://bluefruit.tpondemand.com/api/v1/TestCases/47538?include=[TestSteps[Id]]&format=json&access_token=testaccesstoken"
        ]
    
def test_that_fetcher_gets_a_test_with_test_steps_from_a_feature_with_one_test(fetcher, monkeypatch):
    def mock_get(*args, **kwargs):
        return GetTestStepsSuccessResponse()
    monkeypatch.setattr(requests, "get", mock_get)

    fetcher.test_case_ids = [34566]
    fetcher.construct_test_step_get_requests()

    expected_test_case_with_test_steps = [{
    "ResourceType": "TestCase",
    "Id": 34566,
    "Name": "Scenario: This is a test title",
    "TestSteps": {
        "Items": [
            {
                "ResourceType": "TestStep",
                "Id": 77777,
            },
            {
                "ResourceType": "TestStep",
                "Id": 77778,
            },
            {
                "ResourceType": "TestStep",
                "Id": 77779,
            }
        ]
        }
        }]

    fetcher.get_tests_from_ids()
    assert fetcher.test_cases == expected_test_case_with_test_steps

def test_that_fetcher_gets_all_tests_with_test_steps_from_a_feature_with_multiple_test(fetcher, monkeypatch):
    def mock_get(*args, **kwargs):
        return GetTestStepsSuccessResponse()
    monkeypatch.setattr(requests, "get", mock_get)

    fetcher.test_case_ids = [34566,34566,34566]
    fetcher.construct_test_step_get_requests()

    expected_test_case_with_test_steps = [{
    "ResourceType": "TestCase",
    "Id": 34566,
    "Name": "Scenario: This is a test title",
    "TestSteps": {
        "Items": [
            {
                "ResourceType": "TestStep",
                "Id": 77777,
            },
            {
                "ResourceType": "TestStep",
                "Id": 77778,
            },
            {
                "ResourceType": "TestStep",
                "Id": 77779,
            }
        ]
        }
        },
        {
    "ResourceType": "TestCase",
    "Id": 34566,
    "Name": "Scenario: This is a test title",
    "TestSteps": {
        "Items": [
            {
                "ResourceType": "TestStep",
                "Id": 77777,
            },
            {
                "ResourceType": "TestStep",
                "Id": 77778,
            },
            {
                "ResourceType": "TestStep",
                "Id": 77779,
            }
        ]
        }
        },
        {
    "ResourceType": "TestCase",
    "Id": 34566,
    "Name": "Scenario: This is a test title",
    "TestSteps": {
        "Items": [
            {
                "ResourceType": "TestStep",
                "Id": 77777,
            },
            {
                "ResourceType": "TestStep",
                "Id": 77778,
            },
            {
                "ResourceType": "TestStep",
                "Id": 77779,
            }
        ]
        }
        }]

    fetcher.get_tests_from_ids()
    assert fetcher.test_cases == expected_test_case_with_test_steps

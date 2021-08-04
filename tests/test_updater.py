from tests.test_fetcher import fetcher
from _pytest.monkeypatch import monkeypatch
from pytest import fixture
from unittest import mock
from src.updater import Updater
from src.jsonifier import Jsonifier
from src.reader import Reader
from src.fetcher import Fetcher
import requests

class FeatureCheckSuccessResponse:
    status_code = 200

    @staticmethod
    def json():
        return {"Items": [{"ResourceType": "Feature","Id": 99999}]}

class FeatureCheckFailureResponse:
    status_code = 404

@fixture
def update_test_feature():
    return Updater(Jsonifier(Reader("tests/tagged_feature.feature"), 12345))

# @fixture
# def update_test_fetcher():
#     fetcher = Fetcher(99999)
#     fetcher.test_case_ids = [47543, 34567, 47538]
#     return fetcher

def test_updater_sets_json_feature_file_on_initialisation(update_test_feature):
    expected_local_tp_feature_file = [{
        "Name": "Scenario: This is a test title",
        "ID": 34566,
        "Project":{"ID":12345},
        "TestSteps": 
        {
            "Items": 
            [
                {
                   "ResourceType": "TestStep",
                    "Description": "Given a set up" 
                },
                {
                    "ResourceType": "TestStep",
                    "Description": "When an action occurs"
                },
                {
                    "ResourceType": "TestStep",
                    "Description": "Then there is an outcome"
                }
            ]

         }
     },
     {
        "Name": "Scenario: This is another test title",
        "Project": {"ID": 12345},
        "TestSteps": {
            "Items":[
                {
                    "ResourceType": "TestStep",
                    "Description": "Given a slightly different set up"
                },
                {
                    "ResourceType": "TestStep",
                    "Description": "When a similar action occurs"
                },
                {
                    "ResourceType": "TestStep",
                    "Description": "Then there is a different outcome"
                }
             ]
         }
     },
     {
        "Name": "Scenario: Title test a is this",
        "ID": 34567,
        "Project": {"ID": 12345},
        "TestSteps": {
            "Items":[
                {
                    "ResourceType": "TestStep",
                    "Description": "Given up set a"
                },
                {
                    "ResourceType": "TestStep",
                    "Description": "When occurs action an"
                },
                {
                    "ResourceType": "TestStep",
                    "Description": "Then outcome an is there"
                }
             ]
         }
     },
     {
        "Name": "Scenario: Title test another is this",
        "ID": 34565,
        "Project": {"ID": 12345},
        "TestSteps": {
            "Items":[
                {
                    "ResourceType": "TestStep",
                    "Description": "Given up set different slightly a"
                },
                {
                    "ResourceType": "TestStep",
                    "Description": "When occurs action similar an"
                },
                {
                    "ResourceType": "TestStep",
                    "Description": "Then outcome different a is there"
                }
             ]
         }
     }
     ]

    assert(update_test_feature.local_tp_feature_file == expected_local_tp_feature_file)

def test_updater_constructs_a_request_to_check_existence_of_feature(update_test_feature):
    assert update_test_feature.construct_feature_check_request() == "https://bluefruit.tpondemand.com/api/v1/Features?where=(Name eq \'Feature: Whole Feature\') and (Project.Id eq 12345)&include=[Id]&format=json&access_token=testaccesstoken"

def test_the_feature_file_does_not_exist_in_target_process(update_test_feature, monkeypatch):
    def mock_get(*args, **kwargs):
        return FeatureCheckFailureResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    assert(update_test_feature.does_feature_exist() == False)

def test_the_feature_file_does_exist_in_target_process(update_test_feature, monkeypatch):
    def mock_get(*args, **kwargs):
        return FeatureCheckSuccessResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    assert(update_test_feature.does_feature_exist())

def test_that_updater_creates_a_list_of_duplicate_tests(update_test_feature, monkeypatch):
    def mock_fetcher_extract_test_case_ids_from_feature(*args, **kwargs):
        return [47543, 34567, 47538]
    monkeypatch.setattr(Fetcher, "extract_test_case_ids_from_feature", mock_fetcher_extract_test_case_ids_from_feature)

    update_test_feature.find_tests_that_are_local_and_remote()
    update_test_feature.test_cases_to_update == [34567]
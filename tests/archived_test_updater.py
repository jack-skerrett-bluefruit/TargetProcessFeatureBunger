from _pytest.fixtures import FixtureDef
from pytest import fixture
from src.updater import Updater
from src.jsonifier import Jsonifier
from src.reader import Reader
import requests

class FeatureCheckSuccessResponse:
    status_code = 200

    @staticmethod
    def json():
        return {"Items": [{"ResourceType": "Feature","Id": 99999}]}

class FeatureCheckFailureResponse:
    status_code = 404

class GetFeatureTestCases:
    
    @staticmethod
    def json():
        return {"ResourceType": "Feature","Id": 99999,"LinkedTestPlan": {
            "ResourceType": "TestPlan",
            "Id": 99998,
            "TestCases": {
                "Items": [
                    {"ResourceType": "TestCase","Id": 34565},
                    {"ResourceType": "TestCase","Id": 34566},
                    {"ResourceType": "TestCase","Id": 34567}]}}}


@fixture
def feature_updater():
    return Updater("Feature: Whole Feature", 12345)


@fixture
def non_existent_feature_updater():
    return Updater("Feature: Not A Whole Feature", 12345)

@fixture
def known_feature_to_update():
    updater = Updater("Feature: Whole Feature", 12345)
    updater.feature_id = 99999
    return updater

@fixture
def features_test_cases_are_known():
    updater = Updater("Feature: Whole Feature", 12345)
    updater.feature_id = 99999
    updater.tp_test_cases = [34565, 34566, 34567]
    updater.feature_file = Jsonifier(Reader("tests/tagged_feature.feature"), 12345)
    return updater


@fixture
def features_test_cases_are_unknown():
    updater = Updater("Feature: Whole Feature", 12345)
    updater.feature_id = 99999
    updater.tp_test_cases = []
    updater.feature_file = Jsonifier(Reader("tests/tagged_feature.feature"), 12345)
    return updater


def test_updater_creates_a_request_to_check_that_a_feature_exists(feature_updater):
    assert feature_updater.check_feature_exists_request_url == "https://bluefruit.tpondemand.com/api/v1/Features?where=(Name eq 'Feature: Whole Feature') and (Project.Id eq 12345)&include=[Id]&format=json&access_token=testaccesstoken"


def test_updater_finds_a_feature(feature_updater, monkeypatch):
    def mock_get(*args, **kwargs):
        return FeatureCheckSuccessResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    assert(feature_updater.check_feature() == True)
    

def test_updater_does_not_find_a_feature(non_existent_feature_updater, monkeypatch):
    def mock_get(*args, **kwargs):
        return FeatureCheckFailureResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    assert(non_existent_feature_updater.check_feature() == False)


def test_updater_sets_feature_id_if_a_feature_exists(feature_updater, monkeypatch):
    def mock_get(*args, **kwargs):
        return FeatureCheckSuccessResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    feature_updater.check_feature()
    assert feature_updater.feature_id == 99999
    

def test_updater_gets_a_list_of_test_cases_linked_to_a_known_feature(known_feature_to_update, monkeypatch):
    def mock_get(*args, **kwargs):
        return GetFeatureTestCases()

    expected_response = {"ResourceType": "Feature","Id": 99999,"LinkedTestPlan": {
            "ResourceType": "TestPlan",
            "Id": 99998,
            "TestCases": {
                "Items": [
                    {"ResourceType": "TestCase","Id": 34565},
                    {"ResourceType": "TestCase","Id": 34566},
                    {"ResourceType": "TestCase","Id": 34567}]}}}

    monkeypatch.setattr(requests, "get", mock_get)
    assert known_feature_to_update.get_test_cases_of_an_existing_feature() == expected_response


def test_updater_stores_list_of_all_test_case_ids_of_a_known_feature(known_feature_to_update, monkeypatch):
    def mock_get_test_cases_of_an_existing_feature(*args, **kwargs):
        return {"ResourceType": "Feature","Id": 99999,"LinkedTestPlan": {
            "ResourceType": "TestPlan",
            "Id": 99998,
            "TestCases": {
                "Items": [
                    {"ResourceType": "TestCase","Id": 34565},
                    {"ResourceType": "TestCase","Id": 34566},
                    {"ResourceType": "TestCase","Id": 34567}]}}}
        
    monkeypatch.setattr(Updater, "get_test_cases_of_an_existing_feature", mock_get_test_cases_of_an_existing_feature)
    known_feature_to_update.set_test_cases_of_an_existing_feature()
    assert known_feature_to_update.tp_test_cases == [34565, 34566, 34567]

def test_updater_splits_local_tests_into_ones_with_and_without_ids(features_test_cases_are_known):
    expected_known_tests = [
        {
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
    expected_unknown_tests = [{
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
     }]

    test_lists = features_test_cases_are_known.extract_unknown_tests()
    assert test_lists[0] == expected_known_tests
    assert test_lists[1] == expected_unknown_tests
    




def test_updater_splits_tests_out_that_do_exist_in_target_process_for_a_feature_with_only_knowns(features_test_cases_are_known):
    expected_unknown_test = [{
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
    }]
    
    features_test_cases_are_known.compare_local_feature_with_target_process()
    known_test_cases = []
    for test in features_test_cases_are_known.tests_in_target_process:
        known_test_cases.append(test["ID"])

    known_test_cases.sort()

    assert known_test_cases == [34565, 34566, 34567] 
    assert features_test_cases_are_known.tests_with_id_not_in_target_process == []
    assert features_test_cases_are_known.tests_with_no_id_not_in_target_process == expected_unknown_test

def test_updater_splits_tests_out_that_dont_exist_in_target_process_for_a_feature_with_only_unknowns(features_test_cases_are_unknown):
    features_test_cases_are_unknown.compare_local_feature_with_target_process()
    expected_unknown_test = [{
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
    }]

    features_test_cases_are_unknown.compare_local_feature_with_target_process()

    known_test_cases = []
    for test in features_test_cases_are_unknown.tests_in_target_process:
        known_test_cases.append(test["ID"])


    known_test_cases.sort()

    assert known_test_cases == []
    assert features_test_cases_are_unknown.tests_with_no_id_not_in_target_process == expected_unknown_test

def test_that_updater_finds_tests_that_need_to_be_updated():
    assert(False)

def test_that_updater_updates_the_tests_that_need_updating():
    assert(True)
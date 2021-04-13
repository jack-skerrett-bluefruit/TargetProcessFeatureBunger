from pytest import fixture
from src.updater import Updater
from src.jsonifier import Jsonifier
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
    updater.feature_file = Jsonifier("tests/tagged_feature.feature", 12345)
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

def test_updater_splits_tests_out_that_dont_exist_in_feature(features_test_cases_are_known):
    features_test_cases_are_known.compare_local_feature_with_target_process()
    assert features_test_cases_are_known.tests_in_target_process == [34565, 34566, 34567] 
    assert features_test_cases_are_known.tests_not_in_target_process == []
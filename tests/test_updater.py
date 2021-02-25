from pytest import fixture
from src.updater import Updater
import requests

class FeatureCheckSuccessResponse:
    status_code = 200

class FeatureCheckFailureResponse:
    status_code = 

@fixture
def feature_updater():
    return Updater("Feature: Whole Feature", 99999, 12345)


def test_that_updater_intialises_with_feature_id(feature_updater):
    assert feature_updater.feature_id == 99999


def test_updater_creates_a_request_to_check_that_a_feature_exists(feature_updater):
    assert feature_updater.check_feature_exists_request_url == "https://bluefruit.tpondemand.com/api/v1/Features?where=(Name eq 'Feature: Whole Feature') and (Project.Id eq 12345)&include=[Id]&format=json&access_token=testaccesstoken"


def test_updater_finds_a_feature(feature_updater, monkeypatch):
    def mock_get(*args, **kwargs):
        return FeatureCheckSuccessResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    assert(feature_updater.check_feature() == 200)
    


def test_updater_does_not_find_a_feature():
    def mock_get(*args, **kwargs):
        return FeatureCheckFailureResponse()


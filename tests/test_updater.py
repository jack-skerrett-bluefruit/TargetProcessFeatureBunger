from pytest import fixture
from src.updater import Updater


@fixture
def feature_updater():
    return Updater(99999)

def test_that_updater_intialises_with_feature_id(feature_updater):
    assert feature_updater.feature_id == 99999

def test_updater_creates_a_request_to_check_that_a_feature_exists(feature_updater):
    assert feature_updater.check_feature_exists_request == "https://bluefruit.tpondemand.com/api/v1/Features/99999?include=[Id]&format=json&access_token=testaccesstoken"
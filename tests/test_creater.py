from pytest import fixture
from unittest import mock
from src.creater import Creater
from src.jsonifier import Jsonifier


@fixture
def json_test_feature():
    return Jsonifier("tests/test.feature", 12345)

@fixture
def json_whole_feature():
    return Jsonifier("tests/whole_feature.feature", 12345)

def test_creater_initialises_with_request_url_and_params_for_uploading_test_cases():
    test_case_creater = Creater("TestCases")
    assert test_case_creater.request_url == "https://bluefruit.tpondemand.com/api/v1/TestCases/bulk?include=[ID]&format=json&access_token=testaccesstoken"

@mock.patch("src.creater.requests.post")
def test_creater_uploads_single_test_file(mock_request_post, json_test_feature):
    mock_request_post.return_value = mock.Mock(name = "mock_api_response",
                                                **{"status_code": 200, "json.return_value": '{"Items": [{"ResourceType":"TestCase","Id":12345}]}'})
    test_case_creater = Creater("TestCases", json_test_feature.tp_format_feature_file)
    assert test_case_creater.upload_entity() == (200, 12345)

@mock.patch("src.creater.requests.post")
def test_creater_creates_a_single_feature_entity(mock_request_post, json_whole_feature):
    mock_request_post.return_value = mock.Mock(name = "mock_api_response",
                                                **{"status_code": 200, "json.return_value": '{"Items": [{"ResourceType": "Feature","Id":87596}]}'})
    feature_creater = Creater("Features", json_whole_feature.create_new_feature_or_test_plan_body())
    assert feature_creater.upload_entity() == (200, 87596)

def test_creater_initialises_with_with_request_url_and_params_for_creating_feature():
    feature_creater = Creater("Features")
    assert feature_creater.request_url == "https://bluefruit.tpondemand.com/api/v1/Features/bulk?include=[ID]&format=json&access_token=testaccesstoken"

def test_Creater_initialises_with_request_url_and_params_for_creating_test_plan():
    test_plan_creater = Creater("TestPlans")
    assert test_plan_creater.request_url == "https://bluefruit.tpondemand.com/api/v1/TestPlans/bulk?include=[ID]&format=json&access_token=testaccesstoken"
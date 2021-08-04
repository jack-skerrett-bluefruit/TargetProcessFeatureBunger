from pytest import fixture
from unittest import mock
from src.creator import Creator
from src.jsonifier import Jsonifier
from src.reader import Reader

@fixture
def json_test_feature():
    return Jsonifier(Reader("tests/test.feature"), 12345)

@fixture
def json_whole_feature():
    return Jsonifier(Reader("tests/whole_feature.feature"), 12345)

def test_creator_initialises_with_request_url_and_params_for_uploading_test_cases():
    test_case_creator = Creator("TestCases")
    assert test_case_creator.request_url == "https://bluefruit.tpondemand.com/api/v1/TestCases/bulk?include=[ID]&format=json&access_token=testaccesstoken"

@mock.patch("src.creator.requests.post")
def test_creator_uploads_single_test_file(mock_request_post, json_test_feature):
    mock_request_post.return_value = mock.Mock(name = "mock_api_response",
                                                **{"status_code": 200, "json.return_value": {"Items": [{"ResourceType":"TestCase","Id":12345}]}})
    test_case_creator = Creator("TestCases", json_test_feature.tp_format_feature_file)
    assert test_case_creator.upload_entity() == [12345]

@mock.patch("src.creator.requests.post")
def test_creator_creates_a_single_feature_entity(mock_request_post, json_whole_feature):
    mock_request_post.return_value = mock.Mock(name = "mock_api_response",
                                                **{"status_code": 200, "json.return_value": {"Items": [{"ResourceType": "Feature","Id":99999}]}})
    feature_creator = Creator("Features", json_whole_feature.create_new_feature_or_test_plan_body())
    assert feature_creator.upload_entity() == [99999]

def test_creator_initialises_with_with_request_url_and_params_for_creating_feature():
    feature_creator = Creator("Features")
    assert feature_creator.request_url == "https://bluefruit.tpondemand.com/api/v1/Features/bulk?include=[ID]&format=json&access_token=testaccesstoken"

def test_creator_initialises_with_request_url_and_params_for_creating_test_plan():
    test_plan_creator = Creator("TestPlans")
    assert test_plan_creator.request_url == "https://bluefruit.tpondemand.com/api/v1/TestPlans/bulk?include=[ID]&format=json&access_token=testaccesstoken"

@mock.patch("src.creator.requests.post")
def test_creator_creates_multiple_tests(mock_request_post, json_whole_feature):
    mock_request_post.return_value = mock.Mock(name = "mock_api_response",
                                                **{"status_code": 200, "json.return_value": {"Items": [{"ResourceType":"TestCase","Id":12345},{"ResourceType":"TestCase","Id":12346},{"ResourceType":"TestCase","Id":12347},{"ResourceType":"TestCase","Id":12348}]}})
    test_case_creator = Creator("TestCases", json_whole_feature.tp_format_feature_file)
    assert test_case_creator.upload_entity() == [12345, 12346, 12347, 12348]
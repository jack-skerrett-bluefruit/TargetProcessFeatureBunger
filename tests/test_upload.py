from pytest import fixture
from unittest import mock
from src.upload import Uploader
from src.feature_file_jsonifier import Jsonifier

@fixture
def json_test_feature():
    return Jsonifier("tests/test.feature", 12345)

def test_uploader_initialises_with_request_url_and_params_for_uploading_test_cases():
    test_case_uploader = Uploader("TestCases")
    assert test_case_uploader.request_url == "https://bluefruit.tpondemand.com/api/v1/TestCases/bulk?include=[ID]&format=json&access_token=testaccesstoken"

@mock.patch("src.upload.requests.post")
def test_uploader_uploads_single_test_file(mock_request_post, json_test_feature):
    mock_request_post.return_value = mock.Mock(name = "mock_api_response",
                                                **{"status_code": 200, "json.return_value": '{"Items": [{"ResourceType":"TestCase","Id":12345}]}'})
    test_case_uploader = Uploader("TestCase", json_test_feature.tp_format_feature_file)
    assert test_case_uploader.upload_new_test_cases() == (200, 12345)

@mock.patch("src.upload.requests.post")
def test_uploader_creates_a_single_feature_entity(mock_request_post):
    mock_request_post.return_value = mock.Mock(name = "mock_api_response",
                                                **{"status_code": 200, "json.return_value": '{"Items": [{"ResourceType": "Feature","Id":87596}]'})
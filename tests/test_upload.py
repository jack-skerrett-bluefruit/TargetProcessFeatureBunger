from pytest import fixture
from upload import Uploader
from feature_file_jsonifier import Jsonifier

@fixture
def json_test_feature():
    return Jsonifier("tests/test.feature", 12345)

def test_uploader_initialises_with_request_url_and_params_for_uploading_test_cases():
    test_case_uploader = Uploader("TestCases")
    assert test_case_uploader.request_url == "https://bluefruit.tpondemand.com/api/v1/TestCases/bulk?include=[ID]&access_token=testaccesstoken"

#need to look at implementing mock patch type stuff here
def test_uploader_uploads_single_test_file(json_test_feature):
    server_response = {
        "Items": [
            {
                "ResourceType": "TestCase",
                "Id": 39590,
                "TestPlans": {
                    "Items": []
                    }
            }
        ]
        }

    test_case_uploader = Uploader("TestCase", json_test_feature.tp_format_feature_file)
    assert SOMETHING == SOMETHING


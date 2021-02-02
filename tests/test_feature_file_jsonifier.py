from pytest import fixture
from feature_file_reader import Reader
from feature_file_jsonifier import Jsonifier

@fixture
def json_feature():
    return Jsonifier("tests/test.feature")

def test_jsonifier_initialises_with_a_read_feature_file(json_feature):
    reader = Reader("tests/test.feature")
    reader.set_feature_file()
    json_feature.reader.set_feature_file()
    assert json_feature.reader.file_name == reader.file_name
    assert json_feature.reader.feature_file == reader.feature_file

def test_jsonifier_feature_file_initialises_as_an_empty_dict(json_feature):
    assert type(json_feature.dictionary_feature_file) is dict

def test_jsonifier_converts_a_test_into_a_target_process_friendly_dictionary(json_feature):
    expected_dictionary = {
        "Name": "Scenario: This is a test title",
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
    }
    json_feature.reader.set_feature_file()
    json_feature.set_dictionary_feature_file()
    assert expected_dictionary == json_feature.dictionary_feature_file

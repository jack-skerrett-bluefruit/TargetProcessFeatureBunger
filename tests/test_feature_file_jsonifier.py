from pytest import fixture
from src.feature_file_reader import Reader
from src.feature_file_jsonifier import Jsonifier

@fixture
def json_test_feature():
    return Jsonifier("tests/test.feature", 12345)

@fixture
def json_tests_feature():
    return Jsonifier("tests/tests.feature", 12345)

@fixture
def json_whole_feature_file():
    return Jsonifier("tests/whole_feature.feature", 12345)

def test_jsonifier_initialises_with_a_read_feature_file(json_test_feature):
    read_feature_file = [
        [
            "Scenario: This is a test title",
            "Given a set up",
            "When an action occurs",
            "Then there is an outcome"
        ]
        ]
    assert json_test_feature.reader.file_name == "tests/test.feature"
    assert json_test_feature.reader.feature_file == read_feature_file

def test_jsonifier_feature_file_initialises_as_an_empty_list(json_test_feature):
    assert type(json_test_feature.tp_format_feature_file) is list


def test_jsonifier_converts_mutliple_tests_into_a_target_process_friendly_dictionary_test(json_tests_feature):
    expected_tests= [
        {
        "Name": "Scenario: This is a test title",
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
     }
     ]
    assert expected_tests == json_tests_feature.tp_format_feature_file


def test_jsonifier_converts_a_test_into_a_target_process_friendly_dictionary_test(json_test_feature):
    expected_dictionary = [
        {
        "Name": "Scenario: This is a test title",
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
    }
    ]
    assert expected_dictionary == json_test_feature.tp_format_feature_file

def test_jsonifier_stores_feature_file_name(json_whole_feature_file):
    assert json_whole_feature_file.feature_name == "Feature: Whole Feature"

def test_jsonifier_doesnt_store_a_feature_file_name_if_there_isnt_one_in_the_feature_file(json_tests_feature):
    assert json_tests_feature.feature_name == ""


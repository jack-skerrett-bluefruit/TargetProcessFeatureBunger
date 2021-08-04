from pytest import fixture
from src.reader import Reader
from src.jsonifier import Jsonifier


@fixture
def json_test_feature():
    return Jsonifier(Reader("tests/test.feature"), 12345)

@fixture
def json_tests_feature():
    return Jsonifier(Reader("tests/tests.feature"), 12345)

@fixture
def json_whole_feature_file():
    return Jsonifier(Reader("tests/whole_feature.feature"), 12345)

@fixture
def json_tagged_feature_file():
    return Jsonifier(Reader("tests/tagged_feature.feature"), 12345)

@fixture
def json_tagged_with_strings_feature_file():
    return Jsonifier(Reader("tests/tagged_with_strings.feature"), 12345)

def test_jsonifier_initialises_with_a_read_feature_file(json_test_feature):
    read_feature_file = [
        [
            "Scenario: This is a test title",
            "Given a set up",
            "When an action occurs",
            "Then there is an outcome"
        ]
        ]
    assert json_test_feature.feature_file.file_name == "tests/test.feature"
    assert json_test_feature.feature_file.feature_file == read_feature_file

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
    expected_list = [
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
    assert expected_list == json_test_feature.tp_format_feature_file

def test_jsonifier_stores_feature_file_name(json_whole_feature_file):
    assert json_whole_feature_file.feature_name == "Feature: Whole Feature"

def test_jsonifier_doesnt_store_a_feature_file_name_if_there_isnt_one_in_the_feature_file(json_tests_feature):
    assert json_tests_feature.feature_name == ""

def test_create_new_feature_body(json_whole_feature_file):
    expected_body = [{
        "Name":"Feature: Whole Feature",
        "Project":{"ID":12345}
        }]
    assert json_whole_feature_file.create_new_feature_or_test_plan_body() == expected_body

def test_create_new_test_plan_body(json_whole_feature_file):
    expected_body = [{
        "Name":"Feature: Whole Feature",
        "Project":{"ID":12345}
        }]
    assert json_whole_feature_file.create_new_feature_or_test_plan_body() == expected_body

def test_jsonifier_adds_the_first_tag_as_test_case_id(json_tagged_feature_file):
    expected_tests = [
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
    
    assert expected_tests == json_tagged_feature_file.tp_format_feature_file

def test_that_jsonifier_handles_tags_with_non_numerical_prefixes_or_suffixes(json_tagged_with_strings_feature_file):
    expected_tests = [
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

    assert expected_tests == json_tagged_with_strings_feature_file.tp_format_feature_file
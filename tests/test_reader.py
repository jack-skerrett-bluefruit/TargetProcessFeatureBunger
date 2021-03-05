from pytest import fixture
from src.reader import Reader

@fixture
def test_reader():
    return Reader("tests/test.feature")

@fixture
def tests_reader():
    return Reader("tests/tests.feature")

@fixture
def examples_reader():
    return Reader("tests/examples.feature")

@fixture
def examples_no_spaces_reader():
    return Reader("tests/examples_no_spaces.feature")

@fixture
def whole_feature_file_reader():
    return Reader("tests/whole_feature.feature")

@fixture
def tagged_feature_file_reader():
    return Reader("tests/tagged_feature.feature")

def test_reader_initialises_with_given_feature_file(test_reader):
    assert test_reader.file_name == "tests/test.feature"

def test_reader_stores_test_as_a_list(test_reader):
    assert type(test_reader.feature_file) is list

def test_that_there_is_no_empty_line_between_the_last_step_of_a_test_and_an_examples_table(examples_reader):
    i = -1 
    for line in examples_reader.feature_file:
        if(line == "Examples:"):
            assert examples_reader.feature_file[i] != ""
        i += 1

def test_scenarios_are_stored_as_separate_list_items(tests_reader):
    expected_feature_list = [
        [
            "Scenario: This is a test title",
            "Given a set up",
            "When an action occurs",
            "Then there is an outcome"
        ],
        [
            "Scenario: This is another test title",
            "Given a slightly different set up",
            "When a similar action occurs",
            "Then there is a different outcome"
        ]
    ]
    assert expected_feature_list == tests_reader.feature_file

def test_a_feature_file_with_no_spaces_is_read_in_correctly(examples_no_spaces_reader):
    expected_feature_list = [
        [
            "Scenario: This is another test title",
            "Given a <amount> different set up",
            "When an similar <action> occurs",
            "Then there is a different outcome",
            "Examples:",
            "|amount|action|",
            "|slightly|earthquake|",
            "|slightly|realisation|",
            "|hugely|earthquake|",
            "|hugely|realisation|"
        ]
    ]
    assert expected_feature_list == examples_no_spaces_reader.feature_file

def test_reader_can_read_a_full_feature_file(whole_feature_file_reader):
    expected_feature_list = [
        "Feature: Whole Feature",
        [
            "Scenario: This is a test title",
            "Given a set up",
            "When an action occurs",
            "Then there is an outcome"
        ],
        [
            "Scenario: This is another test title",
            "Given a slightly different set up",
            "When a similar action occurs",
            "Then there is a different outcome"
        ],
        [
            "Scenario: Title test a is this",
            "Given up set a",
            "When occurs action an",
            "Then outcome an is there"
        ],
        [
            "Scenario: Title test another is this",
            "Given up set different slightly a",
            "When occurs action similar an",
            "Then outcome different a is there"
        ]
    ]
    assert whole_feature_file_reader.feature_file == expected_feature_list

def test_reader_adds_tags_above_scenario_titles(tagged_feature_file_reader):
    expected_feature_list = [
        "Feature: Whole Feature",
        [
            "@34566",
            "Scenario: This is a test title",
            "Given a set up",
            "When an action occurs",
            "Then there is an outcome"
        ],
        [
            "Scenario: This is another test title",
            "Given a slightly different set up",
            "When a similar action occurs",
            "Then there is a different outcome"
        ],
        [
            "@34567",
            "Scenario: Title test a is this",
            "Given up set a",
            "When occurs action an",
            "Then outcome an is there"
        ],
        [
            "@34565",
            "Scenario: Title test another is this",
            "Given up set different slightly a",
            "When occurs action similar an",
            "Then outcome different a is there"
        ]
    ]

    assert tagged_feature_file_reader.feature_file == expected_feature_list
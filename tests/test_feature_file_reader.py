from pytest import fixture
from feature_file_reader import Reader

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

def test_reader_initialises_with_given_feature_file(test_reader):
    assert test_reader.file_name == "tests/test.feature"

def test_reader_stores_test_as_a_list(test_reader):
    assert type(test_reader.feature_file) is list

def test_that_there_is_no_empty_line_between_the_last_step_of_a_test_and_an_examples_table(examples_reader):
    i = -1 
    for line in examples_reader.feature_file:
        if(line == "Examples:"):
            assert examples_reader.feature_file[i] is not ""
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
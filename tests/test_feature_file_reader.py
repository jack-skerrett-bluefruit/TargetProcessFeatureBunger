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

def test_reader_initialises_with_given_feature_file(test_reader):
    assert test_reader.file_name == "tests/test.feature"

def test_reader_stores_test_as_a_list(test_reader):
    test_reader.set_feature_file()
    assert type(test_reader.feature_file) is list

def test_reader_stores_each_line_of_a_test_as_a_separate_list_item(test_reader):
    test_reader.set_feature_file()
    with open("tests/test.feature") as f:
        test = f.read().splitlines()
    assert test_reader.feature_file == test

def test_multiple_tests_are_stored_in_a_list_separated_by_a_line(tests_reader):
    tests_reader.set_feature_file()
    with open("tests/tests.feature") as f:
        tests = f.read().splitlines()
    assert tests_reader.feature_file == tests

def test_that_there_is_no_empty_line_between_the_last_step_of_a_test_and_an_examples_table(examples_reader):
    examples_reader.set_feature_file()
    i = -1 
    for line in examples_reader.feature_file:
        if(line == "Examples:"):
            assert examples_reader.feature_file[i] is not ""
        i += 1

def test_that_there_is_an_empty_line_only_between_scenarios(tests_reader):
    tests_reader.set_feature_file()
    i = 1
    for line in tests_reader.feature_file:
        if(line == ""):
            assert tests_reader.feature_file[i][:8] == "Scenario"
        i += 1

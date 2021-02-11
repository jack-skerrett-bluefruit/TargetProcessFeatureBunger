from src.organise_features import Organiser

def test_feature_organiser_initialises_withtest_case_id_and_feature_id_to_assign_it_to():
    feature_organiser = Organiser(54321, 12345)
    assert feature_organiser.feature == 54321
    assert feature_organiser.test_case == 12345

def test_feature_organiser_constructs_correct_data_for_assinging_a_test_case_to_a_feature():
    expected_data = {
        "TestPlans":{
            "Items":[
                {"ID": 54321}
                ]
            }
        }
    
    feature_organiser = Organiser(54321, 12345)
    assert feature_organiser.data == expected_data

def test_feature_organiser_creates_the_correct_url_to_post_assign_data_to():
    expected_url = "https://bluefruit.tpondemand.com/api/v1/TestCases/12345?format=json&access_token=testaccesstoken"
    feature_organiser = Organiser(54321, 12345)
    assert feature_organiser.request_url == expected_url 
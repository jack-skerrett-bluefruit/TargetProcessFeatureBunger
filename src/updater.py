from settings import TP_URL, ACCESS_TOKEN

class Updater:
    def __init__(self, feature_id):
        self.feature_id = feature_id
        self.check_feature_exists_request = self.set_request_url()

    def set_request_url(self):
        return f"{TP_URL}Features/{self.feature_id}?include=[Id]&format=json&access_token={ACCESS_TOKEN}"

import json


class MockPullIncidentReportsSuccessfully:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return [
            {'incident': 'Hello', 'position': 1},
            {'incident': 'Hey', 'position': 1},
            {'incident': 'Hi', 'position': 1},
        ]

    @property
    def content(self):
        return json.dumps(self.json())

    @property
    def number_of_results(self):
        return len(self.json())


class MockPullIncidentReportsNotFound:
    def __init__(self):
        self.status_code = 404

    def json(self):
        return {'detail': 'page not found'}

    @property
    def content(self):
        return json.dumps(self.json())

    # TODO(Feature) dynamic database model for incident report

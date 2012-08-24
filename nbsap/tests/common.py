import unittest

from werkzeug.datastructures import ImmutableDict

from nbsap.app import create_app
from nbsap.database import mongo

class _BaseTest(unittest.TestCase):

    OBJECTIVE_MOCK = {
        "1": ImmutableDict({
            "title": ImmutableDict({
                "en": "Visitor",
                "fr": "Frenche Visitor",
                "nl": "Dutch Visitor"
            }),
            "body": ImmutableDict({
                "en": "Visitor",
                "fr": "French visitor",
                "nl": "Dutch visitor"
            }),
            "id": 1,
            "subobjs": []
    })}

    testing_config = {
        "MONGO_DBNAME": "testing-nbsap",
        "SECRET_KEY": "somwthing random"
    }

    def setUp(self):
       self.app = create_app(testing_config=self.testing_config)
       self.app.config["TESTING"] = True

       self.client = self.app.test_client()

       self._create_objective()

    def tearDown(self):
        with self.app.test_request_context():
            mongo.db.objectives.remove()
            mongo.db.mapping.remove()


    def _create_objective(self):
        mock_objective = dict(self.OBJECTIVE_MOCK['1'])
        with self.app.test_request_context():
            mongo.db.objectives.save(mock_objective)



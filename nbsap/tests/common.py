import unittest

from werkzeug.datastructures import ImmutableDict

from nbsap.app import create_app
from nbsap.database import mongo

class _BaseTest(unittest.TestCase):

    OBJECTIVE_MOCK = {
        "1": ImmutableDict({
            "title": ImmutableDict({
                "en": "Mock objective title",
                "fr": "Frenche mock objective title",
                "nl": "Dutch mock objective title"
            }),
            "body": ImmutableDict({
                "en": "Mock objective body",
                "fr": "French mock objective",
                "nl": "Dutch mock objective"
            }),
            "id": 1,
            "subobjs": []
    })}

    ACTION_MOCK = {
        "1": ImmutableDict({
            "title": ImmutableDict({
                "en": "Mock action",
                "fr": "French mock action",
                "nl": "Dutch mock action"
            }),
            "id": 1,
            "actions": [
                ImmutableDict({
                    "title": ImmutableDict({
                        "en": "Mock title action in subobjective",
                        "fr": "French title mock action in subobjective",
                        "nl": "Dutch title mock action in subobjective"
                    }),
                    "body": ImmutableDict({
                        "en": "Mock body action in subobjective",
                        "fr": "French body mock action in subobjective",
                        "nl": "Dutch body mock action in subobjective"
                    }),
                    "id": 1
                })
            ]
        })
    }

    GOAL_MOCK = {
        "1": ImmutableDict({
            "title": ImmutableDict({
                "en": "Mock goal title",
                "fr": "French mock goal title",
                "nl": "Dutch mock goal title"
            }),
            "id": "1",
            "short_title": "A",
            "description": ImmutableDict({
                "en": "Mock goal description",
                "fr": "French mock goal description",
                "nl": "Dutch mock goal description"
            })
        })
    }

    testing_config = {
        "MONGO_DBNAME": "testing-nbsap",
        "SECRET_KEY": "somwthing random"
    }

    def setUp(self):
       self.app = create_app(testing_config=self.testing_config)
       self.app.config["TESTING"] = True

       self.client = self.app.test_client()

       self._create_objective()
       self._create_action()
       self._create_goal()

    def tearDown(self):
        with self.app.test_request_context():
            mongo.db.objectives.remove()
            mongo.db.actions.remove()
            mongo.db.mapping.remove()
            mongo.db.goals.remove()

    def _create_objective(self):
        mock_objective = dict(self.OBJECTIVE_MOCK['1'])
        with self.app.test_request_context():
            mongo.db.objectives.save(mock_objective)

    def _create_action(self):
        mock_action = dict(self.ACTION_MOCK['1'])
        with self.app.test_request_context():
            mongo.db.actions.save(mock_action)

    def _create_goal(self):
        mock_goal = dict(self.GOAL_MOCK['1'])
        with self.app.test_request_context():
            mongo.db.goals.save(mock_goal)

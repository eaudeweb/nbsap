import unittest
import bson

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
            "subobjs": [
                ImmutableDict({
                    "title": ImmutableDict({
                        "en": "Mock subobjective title",
                        "fr": "Frenche mock subobjective title",
                        "nl": "Dutch mock subobjective title"
                    }),
                    "body": ImmutableDict({
                        "en": "Mock subobjective body",
                        "fr": "French submock objective",
                        "nl": "Dutch mock subobjective"
                    }),
                    "id": 1,
                    "subobjs": [],
                    "actions": []
                }),
                ImmutableDict({
                    "title": ImmutableDict({
                        "en": "Mock2 subobjective title",
                        "fr": "Frenche mock2 subobjective title",
                        "nl": "Dutch mock2 subobjective title"
                    }),
                    "body": ImmutableDict({
                        "en": "Mock2 subobjective body",
                        "fr": "French submock2 objective",
                        "nl": "Dutch mock2 subobjective"
                    }),
                    "id": 2,
                    "subobjs": [],
                    "actions": []
                }),
            ],
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
                        }),

                        ImmutableDict({
                            "title": ImmutableDict({
                                "en": "Mock2 title action in subobjective",
                                "fr": "",
                                "nl": "Dutch title mock action in subobjective"
                            }),
                            "body": ImmutableDict({
                                "en": "Mock body action in subobjective",
                                "fr": "",
                                "nl": "Dutch body mock action in subobjective"
                            }),
                            "id": 2
                        })
            ]
    })}


    INDICATOR_MOCK = {
        "1": ImmutableDict({
            "name": ImmutableDict({
                "en": "Mock indicator name",
                "fr": "French mock indicator name",
                "nl": "Dutch mock indicator name"
            }),
            "question": ImmutableDict({
                "en": "Mock indicator question",
                "fr": "French mock indicator question",
                "nl": "Dutch mock indicator question"
            }),
           "head_indicator": ImmutableDict({
                "en": "Mock indicator head indicator",
                "fr": "French mock indicator head indicator",
                "nl": "Dutch mock indicator head indicator"
            }),
           "sub_indicator": ImmutableDict({
                "en": "Mock indicator sub indicator",
                "fr": "French mock indicator sub indicator",
                "nl": "Dutch mock indicator sub indicator"
            }),
           "other_targets": [],
           "scale": [],
           "classification": ImmutableDict({
                "en": "Mock indicator classification",
                "fr": "French mock indicator classification",
                "nl": "Dutch mock indicator classification"
            }),
           "relevant_target": 1,
           "goal": "A",
           "status": ImmutableDict({
                "en": "Mock indicator status",
                "fr": "French mock indicator status",
                "nl": "Dutch mock indicator status"
            }),
           "sources": ImmutableDict({
                "en": "Mock indicator sources",
                "fr": "French mock indicator sources",
                "nl": "Dutch mock indicator sources"
            }),
           "requirements": ImmutableDict({
                "en": "Mock indicator requirements",
                "fr": "French mock indicator requirements",
                "nl": "Dutch mock indicator requirements"
            }),
           "measurer": ImmutableDict({
                "en": "Mock indicator measurer",
                "fr": "French mock indicator measurer",
                "nl": "Dutch mock indicator measurer"
            }),
            "conventions": "Mock indicator conventions",
            "links": [{ 'url': 'Mock link',
                        'url_name': {   'en': 'Mock link name',
                                        'fr': 'French mock link name',
                                        'nl': 'Dutch mock link name'},
                   }],
            "ease_of_communication": "Low",
            "validity": "Low",
            "sensitivity": "Low",
            "id": 1,
    })}

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

    TARGET_MOCK = {
        "1": ImmutableDict({
            "title": ImmutableDict({
                "en": "Mock target title",
                "fr": "French mock target title",
                "nl": "Dutch mock target title"
            }),
            "id": "1",
            "goal_id": "A",
            "description": ImmutableDict({
                "en": "Mock target description",
                "fr": "French mock target description",
                "nl": "Dutch mock target description"
            })
        })
    }


    MAPPING_MOCK = {
        "1": ImmutableDict({
            "objective": "1.1",
            "_id": bson.objectid.ObjectId(),
            "goal": "A",
            "main_target": "1",
            "other_targets": ["2", "3"]
        })
    }

    testing_config = {
        "MONGO_DBNAME": "testing-nbsap",
        "SECRET_KEY": "something random",
        "BYPASS_LOGIN": True
    }

    def setUp(self):
       self.app = create_app(testing_config=self.testing_config)
       self.app.config["TESTING"] = True

       self.client = self.app.test_client()

       self._create_objective()
       self._create_goal()
       self._create_target()
       self._create_indicator()

    def tearDown(self):
        with self.app.test_request_context():
            mongo.db.objectives.remove()
            mongo.db.mapping.remove()
            mongo.db.goals.remove()
            mongo.db.indicators.remove()
            mongo.db.targets.remove()

    def _create_objective(self):
        mock_objective = dict(self.OBJECTIVE_MOCK['1'])
        with self.app.test_request_context():
            mongo.db.objectives.save(mock_objective)

    def _create_goal(self):
        mock_goal = dict(self.GOAL_MOCK['1'])
        with self.app.test_request_context():
            mongo.db.goals.save(mock_goal)

    def _create_indicator(self):
        mock_indicator = dict(self.INDICATOR_MOCK['1'])
        with self.app.test_request_context():
            mongo.db.indicators.save(mock_indicator)

    def _create_target(self):
        mock_target = dict(self.TARGET_MOCK['1'])
        with self.app.test_request_context():
            mongo.db.targets.save(mock_target)

    def _create_mapping(self):
        mock_mapping = dict(self.MAPPING_MOCK['1'])
        with self.app.test_request_context():
            mongo.db.mapping.save(mock_mapping)

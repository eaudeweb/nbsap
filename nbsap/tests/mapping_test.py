# encoding: utf-8
from common import _BaseTest

class MappingTest(_BaseTest):

    def test_render_page(self):

        response = self.client.get('/admin/mapping')
        self.assertEqual(response.status_code, 200)

    def test_save_data_to_database(self):

        data = {
                "goal": "A",
                "main_target": "1",
                "other_targets": ["2", "3"],
                "objective": "1.1",
               }

        response = self.client.post("/admin/mapping", data=data)
        self.assertIn("Mapping saved", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            mapping = [m for m in mongo.db.mapping.find()]

        self.assertEqual(len(mapping), 1)
        self.assertEqual(mapping[0]['goal'], 'A')

    def test_other_targets_are_optional(self):

        data = {
                "goal": "A",
                "main_target": "1",
                "other_targets": [],
                "objective": "1.1",
               }

        response = self.client.post("/admin/mapping", data=data)
        self.assertIn("Mapping saved", response.data)

    def test_validation(self):

        data = {
                "goal": "Z",
                "main_target": "20",
                "other_targets": [],
                "objective": "1.1",
               }

        response = self.client.post("/admin/mapping", data=data)
        self.assertIn("Z is not a valid value for AICHI strategic goal", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            mapping = [m for m in mongo.db.mapping.find()]

        self.assertEqual(len(mapping), 0)

    def test_goal_target_chain(self):

        data = {
                "goal": "A",
                "main_target": "20",
                "other_targets": [],
                "objective": "1.1",
               }

        response = self.client.post("/admin/mapping", data=data)
        self.assertIn("Target 20 is not related to Goal A", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            mapping = [m for m in mongo.db.mapping.find()]

        self.assertEqual(len(mapping), 0)


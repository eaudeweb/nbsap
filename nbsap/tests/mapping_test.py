# encoding: utf-8
from common import _BaseTest

class MappingTest(_BaseTest):

    def test_render_listing_page(self):

        self._create_mapping()
        response = self.client.get('/admin/mapping')
        self.assertEqual(response.status_code, 200)

    def test_save_new_mapping_data_to_database(self):

        data = {
                "goal": "A",
                "main_target": "1",
                "other_targets": ["2", "3"],
                "objective": "1.1",
                "main_eu_target": "0",
                "eu_actions": [],
             }

        response = self.client.post("/admin/mapping/new", data=data)
        self.assertEqual(response.status_code, 302)

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
                "main_eu_target": "0",
                "eu_actions": [],
      }

        response = self.client.post("/admin/mapping/new", data=data)
        self.assertEqual(response.status_code, 302)

    def test_validation(self):

        data = {
                "goal": "Z",
                "main_target": "20",
                "other_targets": [],
                "objective": "1.1",
                "main_eu_target": "0",
                "eu_actions": [],
        }

        response = self.client.post("/admin/mapping/new", data=data)
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
                "main_eu_target": "0",
                "eu_actions": [],

               }

        response = self.client.post("/admin/mapping/new", data=data)
        self.assertIn("Target 20 is not related to Goal A", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            mapping = [m for m in mongo.db.mapping.find()]

        self.assertEqual(len(mapping), 0)

    def test_render_edit_page_for_an_existing_target(self):
        self._create_mapping()

        from nbsap.database import mongo
        with self.app.test_request_context():
            mapping_id = mongo.db.mapping.find_one({}, {'_id': 1})['_id']

        response = self.client.get("/admin/mapping/%s/edit" % mapping_id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Goal A", response.data)

    def test_edit_an_existing_target(self):
        self._create_mapping()

        from nbsap.database import mongo
        with self.app.test_request_context():
            mapping_id = mongo.db.mapping.find_one({}, {'_id': 1})['_id']

        data = {
                'goal': 'B',
                "main_target": "5",
                "other_targets": [],
                "objective": "1.1",
                "main_eu_target": "0",
                "eu_actions": [],
               }

        response = self.client.post("/admin/mapping/%s/edit" % mapping_id, data=data)
        self.assertEqual(response.status_code, 302)

        with self.app.test_request_context():
            new_mapping = [m for m in mongo.db.mapping.find()]

        self.assertEqual(len(new_mapping), 1)
        self.assertEqual(new_mapping[0]['goal'], 'B')
        self.assertEqual(new_mapping[0]['main_target'], '5')
        self.assertEqual(new_mapping[0]['other_targets'], [])


    def test_delete_an_existing_target(self):
        self._create_mapping()

        from nbsap.database import mongo
        with self.app.test_request_context():
            mapping_id = mongo.db.mapping.find_one({}, {'_id': 1})['_id']

        response = self.client.get("/admin/mapping/%s/delete" % mapping_id)
        self.assertEqual(response.status_code, 405)

        response = self.client.delete("/admin/mapping/%s/delete" % mapping_id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.data)

        with self.app.test_request_context():
            mappings = [m for m in mongo.db.mapping.find()]

        self.assertEqual(len(mappings), 0)


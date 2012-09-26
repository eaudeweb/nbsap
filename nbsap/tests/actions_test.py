# encoding: utf-8
from common import _BaseTest

class ActionListingTest(_BaseTest):

    def test_view_from_objective(self):

        response = self.client.get('/admin/objectives/1')
        self.assertEqual(response.status_code, 200)

        self.assertIn("Mock title action in subobjective", response.data)
        self.assertIn("Mock2 title action in subobjective", response.data)
        self.assertIn("btn-success", response.data)
        self.assertIn("btn-warning", response.data)

    def test_action_render_page(self):

        response = self.client.get('/admin/objectives/1/action/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mock body action in subobjective", response.data)
        self.assertIn("href=\"/admin/objectives/1/"
                      "action/1/edit\">Edit", response.data)

        response = self.client.get('/admin/objectives/1/action/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mock body action in subobjective", response.data)
        self.assertIn("href=\"/admin/objectives/1/"
                      "action/2/edit\">Edit", response.data)


class ActionAddTest(_BaseTest):

    def test_view_from_objective(self):

        response = self.client.get('/admin/objectives/1')
        self.assertEqual(response.status_code, 200)

        self.assertIn("href=\"/admin/objectives/1/"
                      "action/add\">Add action", response.data)

    def test_action_render_page(self):

        response = self.client.get('/admin/objectives/1/action/add')
        self.assertEqual(response.status_code, 200)

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "Testing 1,2,3",
                    "body-en": ""
                }

        response = self.client.post("/admin/objectives/1/action/add", data=mydata)
        self.assertIn("Description is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

    def test_error_message_missing_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "Foo bar action title",
                    "body-en": "Foo bar action body"
                }

        response = self.client.post("/admin/objectives/1/action/add", data=mydata)
        self.assertNotIn("Description is required", response.data)
        self.assertNotIn("Title is required", response.data)
        self.assertIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objective = mongo.db.objectives.find_one_or_404({'id': 1})
            actions = [a for a in objective['actions']]
            added_id = max(v['id'] for idx, v in enumerate(actions))

            try:
                find_action = [a for a in objective['actions']
                               if a['id'] == added_id][0]
            except IndexError:
                self.assertEqual(1,2)
            else:
                self.assertEqual(find_action['title']['en'],
                                 "Foo bar action title")
                self.assertEqual(find_action['body']['en'],
                                 "Foo bar action body")


class ActionEditTest(_BaseTest):

    def test_render_page(self):

        response = self.client.get('/admin/objectives/1/action/1/edit')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/admin/objectives/1/action/2/edit')
        self.assertEqual(response.status_code, 200)

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "Testing 1,2,3",
                    "body-en": ""
                }

        response = self.client.post("/admin/objectives/1/action/1/edit", data=mydata)
        self.assertIn("Description is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objective = mongo.db.objectives.find_one_or_404({'id': 1})
            actions = [a for a in objective['actions']]

        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0]['body']['en'], \
                                    'Mock body action in subobjective')

    def test_error_message_missing_when_body_blank(self):

        mydata = {
                    "language": "nl",
                    "title-nl": "Limit test",
                    "body-nl": ""
                }

        response = self.client.post("/admin/objectives/1/action/1/edit", data=mydata)
        self.assertNotIn("Description is required", response.data)
        self.assertIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objective = mongo.db.objectives.find_one_or_404({'id': 1})
            actions = [a for a in objective['actions']]

        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0]['title']['nl'], "Limit test")
        self.assertEqual(actions[0]['body']['nl'], "")

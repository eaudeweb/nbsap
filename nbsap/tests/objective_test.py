# encoding: utf-8
from common import _BaseTest

class ObjectiveDeleteTest(_BaseTest):

     def test_objectives_render_page(self):

        # add a mock objective and a corresponding sample mapping
        mock_objective = dict(self.OBJECTIVE_MOCK['1'])
        mock_objective['id'] = 2
        mock_mapping = dict(self.MAPPING_MOCK['1'])
        mock_mapping['objective'] = '2.1'
        mock_mapping_id = mock_mapping['_id']

        from nbsap.database import mongo
        with self.app.test_request_context():
            mongo.db.objectives.save(mock_objective)
            mongo.db.mapping.save(mock_mapping)

        # test for correct database insertions
        from nbsap.database import mongo
        with self.app.test_request_context():
            objective = mongo.db.objectives.find_one({'id': 2})
            if objective is not None:
                self.assertIn("Mock objective title", objective['title']['en'])
                self.assertIn("Mock objective body", objective['body']['en'])
            else:
                self.assertEqual(1,2)
            mapping = mongo.db.mapping.find_one({'_id': mock_mapping_id})
            if mapping is not None:
                self.assertIn("A", mapping['goal'])
                self.assertIn("1", mapping['main_target'])
                self.assertIn("2.1", mapping['objective'])
            else:
                self.assertEqual(3,4)

        # erase it
        response = self.client.get('/admin/objectives/2/delete')
        from nbsap.database import mongo
        with self.app.test_request_context():
            objective = mongo.db.objectives.find_one({'id': 2})
            if objective is not None:
                self.assertEqual(1,2)
            mapping = mongo.db.mapping.find_one({'_id': mock_mapping_id})
            if mapping is not None:
                self.assertEqual(3,4)


class ObjectiveListingTest(_BaseTest):

     def test_objectives_render_page(self):

        response = self.client.get('/admin/objectives')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mock objective title", response.data)
        self.assertIn("btn-success", response.data)
        self.assertNotIn("btn-warning", response.data)

class ObjectiveAddTest(_BaseTest):

    def test_view_from_objective_homepage(self):

        response = self.client.get('/admin/objectives')
        self.assertEqual(response.status_code, 200)
        self.assertIn("href=\"/admin/objectives/add\"", response.data)

    def test_subobjective_render_page(self):

        response = self.client.get('admin/objectives/add')
        self.assertEqual(response.status_code, 200)

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "Testing 1,2,3",
                    "body-en": ""
                }

        response = self.client.post("admin/objectives/add", data=mydata)
        self.assertIn("Error in adding an objective.", response.data)
        self.assertIn("Description is required", response.data)
        self.assertNotIn("Objective successfully added.", response.data)

    def test_error_message_missing_when_successfull_add(self):

        mydata = {
                    "language": "en",
                    "title-en": "Foo bar subobjective title",
                    "body-en": "Foo bar subobjective body"
                }

        response = self.client.post("admin/objectives/add", data=mydata)
        self.assertNotIn("Description is required", response.data)
        self.assertNotIn("Title is required", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            tmp_collection = mongo.db.objectives.find().sort('id', -1)
            added_id = tmp_collection[0]['id']
            objective = mongo.db.objectives.find_one_or_404({'id': added_id})

            self.assertIn(mydata['title-en'], objective['title']['en'])
            self.assertIn(mydata['body-en'], objective['body']['en'])


class ObjectiveEditTest(_BaseTest):

    def test_objective_render_page(self):

        response = self.client.get('/admin/objectives/1/edit')
        self.assertEqual(response.status_code, 200)

    def test_error_message_displayed_when_title_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "",
                    "body-en": "Some body text in english"
                 }

        response = self.client.post("/admin/objectives/1/edit", data=mydata)
        self.assertIn("Error in editing an objective.", response.data)
        self.assertIn("Title is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objectives = [o for o in mongo.db.objectives.find()]

        self.assertEqual(len(objectives), 1)
        self.assertEqual(objectives[0]['title']['en'], 'Mock objective title')
        self.assertNotEqual(objectives[0]['body']['en'], 'Some body text in english')

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "Some title text in english",
                    "body-en": ""
                }

        response = self.client.post("/admin/objectives/1/edit", data=mydata)
        self.assertIn("Description is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objectives = [o for o in mongo.db.objectives.find()]

        self.assertEqual(len(objectives), 1)
        self.assertEqual(objectives[0]['body']['en'], 'Mock objective body')
        self.assertNotEqual(objectives[0]['title']['en'], 'Some title text in english')

    def test_error_message_missing_when_title_blank(self):

        mydata = {
                    "language": "fr",
                    "title-fr": "",
                    "body-fr": "some text in french"
                }

        response = self.client.post("/admin/objectives/1/edit", data=mydata)
        self.assertNotIn("Title is required", response.data)
        self.assertIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objectives = [o for o in mongo.db.objectives.find()]

        self.assertEqual(len(objectives), 1)
        self.assertEqual(objectives[0]['body']['fr'], 'some text in french')
        self.assertEqual(objectives[0]['title']['fr'], '')


    def test_error_message_missing_when_body_blank(self):

        mydata = {
                    "language": "nl",
                    "title-nl": "sommige platte tekst in het Frans",
                    "body-nl": ""
                }

        response = self.client.post("/admin/objectives/1/edit", data=mydata)
        self.assertNotIn("Body is required", response.data)
        self.assertIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objectives = [o for o in mongo.db.objectives.find()]

        self.assertEqual(len(objectives), 1)
        self.assertEqual(objectives[0]['body']['nl'], '')
        self.assertEqual(objectives[0]['title']['nl'], 'sommige platte tekst in het Frans')


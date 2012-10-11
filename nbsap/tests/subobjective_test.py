# encoding: utf-8
from common import _BaseTest

class SubobjectiveListingTest(_BaseTest):

    def test_view_from_objective(self):

        response = self.client.get('/admin/objectives/1')
        self.assertEqual(response.status_code, 200)

        self.assertIn("Mock subobjective title", response.data)
        self.assertIn("Mock2 subobjective title", response.data)
        self.assertIn("href=\"/admin/objectives/1/1/"
                      "edit?lang=nl\"", response.data)
        self.assertIn("href=\"/admin/objectives/1/2/"
                      "edit?lang=nl\"", response.data)


    def test_subobjective_render_page(self):

        response = self.client.get('/admin/objectives/1/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mock subobjective title", response.data)
        self.assertIn("Mock subobjective body", response.data)
        self.assertIn("href=\"/admin/objectives/1/1/"
                      "edit\">Edit", response.data)
        self.assertIn("href=\"/admin/objectives/1/1/"
                      "add_subobj\"", response.data)
        self.assertIn("href=\"/admin/objectives/1/1/"
                      "action/add\"", response.data)

        response = self.client.get('/admin/objectives/1/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mock2 subobjective title", response.data)
        self.assertIn("Mock2 subobjective body", response.data)
        self.assertIn("href=\"/admin/objectives/1/2/"
                      "edit\">Edit", response.data)
        self.assertIn("href=\"/admin/objectives/1/2/"
                      "add_subobj\"", response.data)
        self.assertIn("href=\"/admin/objectives/1/2/"
                      "action/add\"", response.data)

    def test_subobjective_languages(self):
        response = self.client.get('/admin/objectives/1/1')
        self.assertIn("Mock subobjective title", response.data)
        self.assertIn("Mock subobjective body", response.data)
        respose = self.client.get('/set_language?language=fr')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/admin/objectives/1/1')
        self.assertIn("Frenche mock subobjective title", response.data)
        self.assertIn("French submock objective", response.data)
        respose = self.client.get('/set_language?language=nl')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/admin/objectives/1/1')
        self.assertIn("Dutch mock subobjective title", response.data)
        self.assertIn("Dutch mock subobjective", response.data)
        respose = self.client.get('/set_language?language=en')
        self.assertEqual(response.status_code, 200)


class SubobjectiveAddTest(_BaseTest):

    def test_view_from_objective(self):

        response = self.client.get('/admin/objectives/1')
        self.assertEqual(response.status_code, 200)

        self.assertIn("href=\"/admin/objectives/1/"
                      "add_subobj\"", response.data)

    def test_subobjective_render_page(self):

        response = self.client.get('/admin/objectives/1/add_subobj')
        self.assertEqual(response.status_code, 200)

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "Testing 1,2,3",
                    "body-en": ""
                }

        response = self.client.post("/admin/objectives/1/add_subobj", data=mydata)
        self.assertIn("Error in adding an subobjective.", response.data)
        self.assertIn("Description is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

    def test_error_message_missing_when_successfull_add(self):

        mydata = {
                    "language": "en",
                    "title-en": "Foo bar subobjective title",
                    "body-en": "Foo bar subobjective body"
                }
        response = self.client.post("/admin/objectives/1/add_subobj", data=mydata)

        self.assertNotIn("Description is required", response.data)
        self.assertNotIn("Title is required", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objective = mongo.db.objectives.find_one_or_404({'id': 1})
            subobjs = [s for s in objective['subobjs']]
            added_id = max(v['id'] for idx, v in enumerate(subobjs))

            try:
                find_subobj = [s for s in objective['subobjs']
                               if s['id'] == added_id][0]
            except IndexError:
                self.assertEqual(1,2)
            else:
                self.assertEqual(find_subobj['title']['en'],
                                 "Foo bar subobjective title")
                self.assertEqual(find_subobj['body']['en'],
                                 "Foo bar subobjective body")

    def test_successfull_add_from_subobjective(self):

        mydata = {
                    "language": "en",
                    "title-en": "Foo bar subobjective title",
                    "body-en": "Foo bar subobjective body"
                }
        response = self.client.post("/admin/objectives/1/1/add_subobj", data=mydata)

        self.assertNotIn("Description is required", response.data)
        self.assertNotIn("Title is required", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objective = mongo.db.objectives.find_one_or_404({'id': 1})
            subobjs = [s for s in objective['subobjs']]
            try:
                subobjective = [s for s in subobjs if s['id'] == 1][0]
            except IndexError:
                self.assertEqual(1,2)

            subobjs = [s for s in subobjective['subobjs']]
            added_id = max(v['id'] for idx, v in enumerate(subobjs))

            try:
                find_subobj = [s for s in subobjective['subobjs']
                               if s['id'] == added_id][0]
            except IndexError:
                self.assertEqual(1,2)
            else:
                self.assertEqual(find_subobj['title']['en'],
                                 "Foo bar subobjective title")
                self.assertEqual(find_subobj['body']['en'],
                                 "Foo bar subobjective body")

            response = self.client.get('/admin/objectives/1/1/1')
            self.assertIn("Foo bar subobjective title", response.data)
            self.assertIn("Foo bar subobjective body", response.data)

            respose = self.client.get('/set_language?language=fr')
            self.assertEqual(response.status_code, 200)
            response = self.client.get('/admin/objectives/1/1/1')
            self.assertIn("Foo bar subobjective title", response.data)
            self.assertIn("Foo bar subobjective body", response.data)

            respose = self.client.get('/set_language?language=nl')
            self.assertEqual(response.status_code, 200)
            response = self.client.get('/admin/objectives/1/1/1')
            self.assertIn("Foo bar subobjective title", response.data)
            self.assertIn("Foo bar subobjective body", response.data)



class SubobjectiveEditTest(_BaseTest):

    def test_render_page(self):

        response = self.client.get('/admin/objectives/1/1/edit')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/admin/objectives/1/2/edit')
        self.assertEqual(response.status_code, 200)

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "Testing 1,2,3",
                    "body-en": ""
                }

        response = self.client.post("/admin/objectives/1/1/edit", data=mydata)
        self.assertIn("Description is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objective = mongo.db.objectives.find_one_or_404({'id': 1})
            subobjs = [s for s in objective['subobjs']]

        self.assertEqual(len(subobjs), 2)
        self.assertEqual(subobjs[0]['body']['en'], \
                                    'Mock subobjective body')

    def test_error_message_missing_when_body_blank(self):

        mydata = {
                    "language": "nl",
                    "title-nl": "Limit test",
                    "body-nl": ""
                }

        response = self.client.post("/admin/objectives/1/1/edit", data=mydata)
        self.assertNotIn("Description is required", response.data)
        self.assertIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objective = mongo.db.objectives.find_one_or_404({'id': 1})
            subobjs = [s for s in objective['subobjs']]

        self.assertEqual(len(subobjs), 2)
        self.assertEqual(subobjs[0]['title']['nl'], "Limit test")
        self.assertEqual(subobjs[0]['body']['nl'], "")

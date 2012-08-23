# encoding: utf-8
import unittest

class ObjectiveEditTest(unittest.TestCase):
    def test_error_message_displayed_when_title_blank(self):

        from nbsap.app import create_app
        app = create_app()
        app.config["TESTING"] = True
        app.config["MONGO_DBNAME"] = app.config["TESTING_DBNAME"]

        client = app.test_client()
        mydata = {
                    "language": "en",
                    "title-en": "",
                    "body-en": "Some body text in english"
                 }
        response = client.post("/objective/1/edit", data=mydata)
        html = response.data
        self.assertIn("English is required", html)

    def test_error_message_displayed_when_body_blank(self):

        from nbsap.app import create_app
        app = create_app()
        app.config["TESTING"] = True

        client = app.test_client()
        mydata = {
                    "language": "en",
                    "title-en": "Some title text in english",
                    "body-en": ""
                }
        response = client.post("/objective/1/edit", data=mydata)
        html = response.data
        self.assertIn("English is required", html)

    def test_error_message_missing_when_title_blank(self):

        from nbsap.app import create_app
        app = create_app()
        app.config["TESTING"] = True

        client = app.test_client()
        mydata = {
                    "language": "fr",
                    "title-fr": "",
                    "body-fr": "certains corps de texte en français"
                }
        response = client.post("/objective/1/edit", data=mydata)
        html = response.data
        self.assertNotIn("English is required", html)

    def test_error_message_missing_when_body_blank(self):

        from nbsap.app import create_app
        app = create_app()
        app.config["TESTING"] = True

        client = app.test_client()
        mydata = {
                    "language": "nl",
                    "title-nl": "sommige platte tekst in het Frans",
                    "body-nl": ""
                }
        response = client.post("/objective/1/edit", data=mydata)
        html = response.data
        self.assertNotIn("English is required", html)


# encoding: utf-8
from common import _BaseTest
from nbsap import shell
from nbsap.database import mongo

class ShellTest(_BaseTest):

    def test_indicator_link_list_to_dict(self):
        indicator = { 'id': '10',
                      'links': [['link_name_1', 'url_1'], ['link_name_2', 'url_2']]
                    }

        with self.app.test_request_context():
            mongo.db.indicators.remove()
            mongo.db.indicators.save(indicator)
            shell.indicator_link_list_to_dict()
            indicator = mongo.db.indicators.find_one_or_404({'id': '10'})

        self.assertEqual(type(indicator['links'][0]), dict)
        self.assertEqual(indicator['links'][0]['url_name'], 'link_name_1')
        self.assertEqual(indicator['links'][1]['url_name'], 'link_name_2')
        self.assertEqual(indicator['links'][0]['url'], 'url_1')
        self.assertEqual(indicator['links'][1]['url'], 'url_2')

    def test_split_scale_in_list(self):
        indicator = { 'id': '10',
                      'scale': 'G, R, N'
                    }

        with self.app.test_request_context():
            mongo.db.indicators.save(indicator)
            shell.split_scale_in_list()
            indicator = mongo.db.indicators.find_one_or_404({'id': '10'})

        self.assertEqual(len(indicator['scale']), 3)
        self.assertEqual(indicator['scale'], ['G', 'R', 'N'])

    def test_convert_indicator_ids_to_int(self):
        indicator = {'id': '10'}

        with self.app.test_request_context():
            mongo.db.indicators.save(indicator)
            shell.convert_indicator_ids_to_int()
            indicator = mongo.db.indicators.find_one_or_404({'id': 10})

        self.assertEqual(indicator['id'], 10)
        self.assertEqual(type(indicator['id']), int)


    def test_clean_whitespace(self):
        goal = { 'title': 'Mock title',
                 'description': { 'en': 'Mock description\n\n',
                                  'fr': '\n\n',
                                  'nl': '\n\n'
                        }
                 }

        target = { 'title': 'Mock title',
                    'description': { 'en': 'Mock description\n\n',
                                     'fr': '\n\n',
                                     'nl': '\n\n'
                        }
                 }

        with self.app.test_request_context():
            mongo.db.targets.save(target)
            mongo.db.goals.save(goal)

            shell.clean_whitespace()

            target = mongo.db.targets.find_one_or_404({'title': 'Mock title'})
            goal = mongo.db.goals.find_one_or_404({'title': 'Mock title'})

        self.assertEqual(goal['description']['en'], 'Mock description\n\n')
        self.assertEqual(goal['description']['fr'], '')
        self.assertEqual(goal['description']['nl'], '')
        self.assertEqual(target['description']['en'], 'Mock description\n\n')
        self.assertEqual(target['description']['fr'], '')
        self.assertEqual(target['description']['nl'], '')

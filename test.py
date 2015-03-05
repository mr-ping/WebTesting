import unittest

from log import Log

class LogTest(unittest.TestCase):
    def test_get_last_logs_one(self):
        file = '/var/log/siege.log'
        content = Log.get_last_logs(file, 121)
        content_list = content.split(",")
        self.assertEqual(len(content_list), 10)

    def test_get_last_logs_three(self):
        file = '/var/log/siege.log'
        content = Log.get_last_logs(file, 121, 3)
        content_list = content.split(",")
        self.assertEqual(len(content_list), 28)

    def test_add_new_log(self):
        import os
        #from StringIO import StringIO
        #file = StringIO()
        file = 'unittest_new_log'
        text = 'test content which will be writed to the file'
        for i in range(2):
            Log.add_new_log(file, text)
        try:
            with open(file, 'r') as f:
                self.assertEqual(f.read(), text*2)
        finally:
            os.remove(file)

    def test_get_last_fails_rate(self):
        log = Log('/var/log/siege.log')
        rate = log.get_last_fails_rate(3)
        self.assertIsInstance(rate, float)
        self.assertTrue(rate>=0 and rate<=1)

    def test_get_groups(self):
        log = Log('sync.log')
        groups = log._get_groups()
        self.assertIsInstance(groups, dict)

    def test_get_steps_fails_rate(self):
        log = Log('sync.log')
        groups = log.get_steps_fails_rate()
        self.assertIsInstance(groups, dict)

    def test_get_steps_trans_rate(self):
        log = Log('sync.log')
        groups = log.get_steps_trans_rate()
        self.assertIsInstance(groups, dict)


from chat import Trend
class TrendTest(unittest.TestCase):
    def test_get_points(self):
        log = Log('sync.log')
        fails_rate_dict = log.get_steps_fails_rate()

        trend = Trend('test title',
                      'xlabel name',
                      'ylabel name',
                      'r',
                      2,
                      'line')
        trend.get_points(fails_rate_dict)
        self.assertIsNotNone(trend.xcoordinates)
        self.assertIsNotNone(trend.ycoordinates)


import main
class UrlSourceTest(unittest.TestCase):
    def test_check_url_source_neither(self):
        main.url = None
        main.url_file = None
        res = main.check_url_source()
        self.assertIsNone(res)
        self.assertFalse(main.plotting)

    def test_check_url_source_both(self):
        main.url = True
        main.url_file = True
        res = main.check_url_source()
        self.assertIsNone(res)
        self.assertFalse(main.plotting)

    def test_check_url_source_url(self):
        main.url = 'url_command'
        main.url_file = None
        main.plotting = True
        res = main.check_url_source()
        self.assertEqual(res, 'address')
        self.assertTrue(main.plotting)

    def test_check_url_source_file(self):
        main.url = None
        main.url_file = 'test.py'
        main.plotting = True
        res = main.check_url_source()
        self.assertEqual(res, 'file')
        self.assertTrue(main.plotting)


#class OutlierTest(unittest.TestCase):
#    def test_remove_outlier(self):
#        results = (10, 11, 9, 9, 23)

if __name__ == '__main__':
    unittest.main()

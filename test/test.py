
import io
import unittest
import tinyconfig

class myconfig(tinyconfig.ConfigDict):
    myopt = tinyconfig.Option('foo')
    boolopt = tinyconfig.Option(False, type=tinyconfig.boolean)
    intopt = tinyconfig.Option(9000, type=int)
    listopt = tinyconfig.Option([2,3,5,7], type=int)

teststr = """myopt=astring
# some comment here
boolopt=on
intopt = 42
quoted= "You must now cut down the tallest tree..."
noargs
listopt = 11,13, 17 19
"""

class TestConfigDict(unittest.TestCase):
    def setUp(self):
        self.config = myconfig()

    def test_default(self):
        self.assertEqual(self.config.get('myopt'), 'foo')

    def test_option_autoname(self):
        self.assertEqual(self.config._opts['myopt'].name, 'myopt')


class Test_parse(unittest.TestCase):
    def setUp(self):
        self.config = myconfig()
        tinyconfig.parse_file(io.StringIO(teststr), self.config)

    def test_conf(self):
        self.assertIs(self.config['boolopt'], True)
        self.assertEqual(self.config['intopt'], 42)
        self.assertIs(self.config['noargs'], None)
        self.assertEqual(self.config['quoted'],
                            'You must now cut down the tallest tree...')
        # 11+13+17+19=60
        self.assertEqual(sum(self.config['listopt']), 60)
        self.assertIsInstance(self.config['listopt'][0], int)

class Test_helpers(unittest.TestCase):

    def test_boolean(self):
        self.assertIs(tinyconfig.boolean('true'), True)
        self.assertIs(tinyconfig.boolean('on'), True)
        self.assertIs(tinyconfig.boolean('yes'), True)
        self.assertIs(tinyconfig.boolean('1'), True)
        self.assertIs(tinyconfig.boolean('ytughjghf'), False)

if __name__ == '__main__':
    unittest.main()

from unittest import TestCase
import unittest
from ytcutter import YTCutter
import json
from os import path


class TestYTCutter(TestCase):
    @unittest.skip("Don't test it unless you changed something there.")
    def test_download(self):
        self.assertEqual(0, YTCutter().download('https://www.youtube.com/watch?v=ldwg3eXiISM'))

    def test_cut(self):
        ytc = YTCutter()
        with open('test_data/cutdata.json', 'r') as f:
            data = json.load(f)
        filename = 'ALEX & Tokyo Rose - AKUMA [Full Album] 2017-ldwg3eXiISM.opus'
        output_dir = 'testout'
        ytc.cut(filename, data, output_dir)

        for track in data:
            self.assertEqual(True, path.isfile('{0}\\{1}.opus'.format(output_dir, track['name'])))

    def test_run(self):
        ytc = YTCutter()
        with open('test_data/input.json', 'r') as f:
            data = json.load(f)

        ytc.run([data])


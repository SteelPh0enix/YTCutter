from unittest import TestCase
import unittest
from ytcutter import YTCutter
import json
from os import path


class TestYTCutter(TestCase):
    @unittest.skip("This test downloads the track. Don't use, unless you changed something important.")
    def test_download(self):
        self.assertEqual(0, YTCutter().download('https://www.youtube.com/watch?v=ldwg3eXiISM'))

    @unittest.skip("This test needs downloaded track in script directory. Run other test before it.")
    def test_cut(self):
        ytc = YTCutter()
        with open('test_data/cutdata.json', 'r') as f:
            data = json.load(f)
        filename = 'ALEX & Tokyo Rose - AKUMA [Full Album] 2017-ldwg3eXiISM.opus'
        output_dir = 'testout'
        ytc.cut(filename, data, output_dir)

        for track in data:
            self.assertEqual(True, path.isfile('{0}\\{1}.opus'.format(output_dir, track['name'])))

    @unittest.skip("This test downloads the track. Don't use, unless you changed something important.")
    def test_run(self):
        ytc = YTCutter()
        with open('test_data/input.json', 'r') as f:
            data = json.load(f)

        ytc.run([data])

    @unittest.skip("This test downloads the track. Don't use, unless you changed something important.")
    def test_auto_track_recognize_run(self):
        ytc = YTCutter()
        ytc.run([{'url': 'https://www.youtube.com/watch?v=ldwg3eXiISM'}])

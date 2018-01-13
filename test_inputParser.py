from unittest import TestCase
from input_parser import InputParser
import json


class TestInputParser(TestCase):
    def test_calc_duration(self):
        self.assertEqual('0:01:00', InputParser.calc_duration('0:0', '1:0'))
        self.assertEqual('0:10:10', InputParser.calc_duration('10:10', '20:20'))
        self.assertEqual('0:00:00', InputParser.calc_duration('20:10', '20:10'))

    def test_parse_video(self):
        video = {
            "url": "https://www.youtube.com/watch?v=ldwg3eXiISM",
            "tracklist": [{
                "name": "ALEX - Insert Soul",
                "start": "00:00"},

                {"name": "Tokyo Rose - The Pact (feat. WVLFPAKT)",
                 "start": "01:47"},

                {"name": "ALEX - Ritual",
                 "start": "05:16"}]
            }

        parsed = InputParser().parse_video(video)
        expected = {
            'url': 'https://www.youtube.com/watch?v=ldwg3eXiISM',
            'filename': 'ALEX & Tokyo Rose - AKUMA [Full Album] 2017-ldwg3eXiISM.webm',
            'output_dir': 'ALEX & Tokyo Rose - AKUMA [Full Album] 2017',
            'tracklist': [{
                    'name': 'ALEX - Insert Soul',
                    'start': '00:00',
                    'duration': '0:01:47'},
                {
                    'name': 'Tokyo Rose - The Pact (feat. WVLFPAKT)',
                    'start': '01:47',
                    'duration': '0:03:29'},
                {
                    'name': 'ALEX - Ritual',
                    'start': '05:16',
                    'duration': None
                }]
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_tracks(self):
        tracklist = [
            {'name':       'Track 1',
             'start': '00:00'},

            {'name':       'Track 2',
             'start': '01:00'},

            {'name':       'Track 3',
             'start': '05:30'},
        ]
        parsed = InputParser().parse_tracks(tracklist)
        expected = [
            {'name':     'Track 1',
             'start':    '00:00',
             'duration': '0:01:00'},

            {'name':     'Track 2',
             'start':    '01:00',
             'duration': '0:04:30'},

            {'name':     'Track 3',
             'start':    '05:30',
             'duration': None}
        ]
        self.assertListEqual(expected, parsed)

    def test_parse_input(self):
        with open('test_data/input.json') as f:
            input_data = json.load(f)

        with open('test_data/output.json', 'r') as f:
            expected = json.load(f)

        parsed = InputParser().parse_input([input_data])[0]
        self.assertDictEqual(expected, parsed)

    def test_get_filename(self):
        good_filename = 'ALEX & Tokyo Rose - AKUMA [Full Album] 2017-ldwg3eXiISM.webm'
        url = 'https://www.youtube.com/watch?v=ldwg3eXiISM'
        filename = InputParser.get_filename(url)
        self.assertEqual(good_filename, filename)

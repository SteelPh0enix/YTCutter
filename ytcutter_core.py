"""YouTube downloader and cutter"""
from __future__ import unicode_literals
import os
import glob
import youtube_dl
from input_parser import InputParser
from ffmpeg import FFmpeg


class CouldNotReadTracksException(Exception):
    pass


class YTCutter(object):
    """Cutter class"""

    def __init__(self):
        self.musicdata = []
        self.ydl_options = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
            }]
        }
        self.dataparser = InputParser()

    def download(self, url):
        """Get audio from YouTube"""
        with youtube_dl.YoutubeDL(self.ydl_options) as downloader:
            return downloader.download([url])

    @staticmethod
    def cut(filename, cutdata, output_dir):
        """Cut the file according to cutdata dict list
        Cutdata dict list should look like this:
        [{
            'start_point': 'starting point of track'
            'duration': 'duration to cut, None if should be cut to end'
            'output_file': 'path to output file (with extension)'
        }]
        """
        ff = FFmpeg()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        extension = filename.rsplit('.', 1)[1]
        for track in cutdata:
            out = ff.extract(filename, track['start'],
                             track['duration'], "{0}\\{1}.{2}".format(output_dir, track['name'], extension))
            if out.returncode != 0:
                print("FFmpeg returned with code {0}".format(out.returncode))
                print(out.stdout)
    @staticmethod
    def find_audio_file(filename):
        for file in os.listdir(os.getcwd()):
            if file.startswith(filename) and not file.endswith('.part'):
                return file

    def run(self, input_data):
        """Run the cutter with raw input data"""
        parsed = self.dataparser.parse_input(input_data)
        if parsed is None:
            raise CouldNotReadTracksException

        for video in parsed:
            audio_file = self.find_audio_file(video['filename'])

            if audio_file is None:
                self.download(video['url'])
                audio_file = self.find_audio_file(video['filename'])

            self.cut(audio_file, video['tracklist'], video['output_dir'])
            print("Downloaded video and cutted to {2} tracks.\n"
                  "Original file is {0}\n"
                  "Tracks are in {1}\\ directory.".format(audio_file,
                                                          video['output_dir'],
                                                          len(video['tracklist'])))

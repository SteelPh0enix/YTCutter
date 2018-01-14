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

    def run(self, input_data):
        """Run the cutter with raw input data"""
        parsed = self.dataparser.parse_input(input_data)
        if parsed is None:
            raise CouldNotReadTracksException

        for video in parsed:
            self.download(video['url'])

            video_file_glob = glob.glob("{0}.*".format(video['filename']))
            if video_file_glob[0].rsplit('.', 1)[1] == 'part':
                video_file = video_file_glob[1]
            else:
                video_file = video_file_glob[0]

            self.cut(video_file, video['tracklist'], video['output_dir'])
            print("Downloaded video and cutted to {2} tracks.\n"
                  "Original file is {0}\n"
                  "Tracks are in {1}\\ directory.".format(video_file,
                                                          video['output_dir'],
                                                          len(video['tracklist'])))

"""YouTube downloader and cutter"""
from __future__ import unicode_literals
import os
import youtube_dl
from input_parser import InputParser
from ffmpeg import FFmpeg


class YTLogger(object):
    """Logger for youtube_dl"""

    def debug(self, msg):
        """Print debug"""
        print("[DEBUG] " + msg)

    def warning(self, msg):
        """Print warning"""
        print("[WARNING] " + msg)

    def error(self, msg):
        """Print error"""
        print("[ERROR] " + msg)


def yt_hook(data):
    """Hook for youtube_dl"""
    if data['status'] == 'finished':
        print("Downloading {0} finished".format(data['filename']))


class YTCutter(object):
    """Cutter class"""

    def __init__(self):
        self.musicdata = []
        self.ydl_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus'
            }],
            'logger': YTLogger(),
            'progress_hooks': [yt_hook],
        }
        self.dataparser = InputParser()

    def download(self, url):
        """Get audio from YouTube"""
        with youtube_dl.YoutubeDL(self.ydl_options) as downloader:
            return downloader.download([url])

    def cut(self, filename, cutdata, output_dir):
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

        for track in cutdata:
            out = ff.extract_opus(filename, track['start'],
                                  track['duration'], "{0}\\{1}.opus".format(output_dir, track['name']))
            if out.returncode != 0:
                print("FFmpeg returned with code {0}".format(out.returncode))
                print(out.stdout)

    def run(self, input_data):
        """Run the cutter with raw input data"""
        parsed = self.dataparser.parse_input(input_data)
        for video in parsed:
            self.download(video['url'])
            video_opus_name = "{0}.opus".format(video['filename'].rsplit('.')[0])
            self.cut(video_opus_name, video['tracklist'], video['output_dir'])
            print("Downloaded video and cutted to {2} tracks.\n"
                  "Original file is {0}\n"
                  "Tracks are in {1}\\ directory.".format(video_opus_name,
                                                          video['output_dir'],
                                                          len(video['tracklist'])))

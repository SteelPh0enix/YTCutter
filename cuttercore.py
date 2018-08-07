import json

class CutterCore:
    def __init__(self):
        pass

    def download_videos(self, urls):
        for video in urls:
            self.download_video(video)

    def download_video(self, url):
        print("Downloading video {0}".format(url))

    def parse_files(self, files):
        for file in files:
            self.parse_file(file)
            
    def parse_file(self, file):
        print("Parsing from {0}".format(file))
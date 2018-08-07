import json

class CutterCore:
    def __init__(self):
        pass

    def download_videos(self, urls, delete_original):
        for video in urls:
            self.download_video(video, delete_original)

    def download_video(self, url, delete_original):
        print("Downloading video {0}".format(url))

    def parse_files(self, files, delete_original):
        for file in files:
            self.parse_file(file, delete_original)
            
    def parse_file(self, file, delete_original):
        print("Parsing from {0}".format(file))
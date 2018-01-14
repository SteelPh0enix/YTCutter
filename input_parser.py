"""Data parser for the cutter"""
from datetime import datetime
import youtube_dl
import unicodedata
import string

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)


def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    """Took from https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8"""
    # replace spaces
    for r in replace:
        filename = filename.replace(r, ' ')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    return ''.join(c for c in cleaned_filename if c in whitelist)


class InputParser(object):
    def __init__(self):
        self.ytdl_options = {'format': 'bestaudio/best', 'quiet': True, 'simulate': True}

    @staticmethod
    def calc_duration(start: str, end: str) -> str:
        try:
            start_time = datetime.strptime(start, "%M:%S")
        except ValueError:
            try:
                start_time = datetime.strptime(start, "%M:%S.%f")
            except ValueError:
                try:
                    start_time = datetime.strptime(start, "%H:%M:%S")
                except ValueError:
                    start_time = datetime.strptime(start, "%H:%M:%S.%f")

        try:
            end_time = datetime.strptime(end, "%M:%S")
        except ValueError:
            try:
                end_time = datetime.strptime(end, "%M:%S.%f")
            except ValueError:
                try:
                    end_time = datetime.strptime(end, "%H:%M:%S")
                except ValueError:
                    end_time = datetime.strptime(end, "%H:%M:%S.%f")

        return str(end_time - start_time)

    def parse_video(self, video: dict):
        video_info = self.get_video_info(video['url'])
        ret = dict()
        ret['url'] = video['url']
        ret['filename'] = self.get_filename(video_info).rsplit('.', 1)[0]
        ret['output_dir'] = ret['filename'].rsplit('-', 1)[0]

        if 'tracklist' not in video:
            tracklist = self.get_track_list(video_info)
            if tracklist is not None:
                ret['tracklist'] = self.parse_tracks_from_video(tracklist)
                return ret
            else:
                return None

        ret['tracklist'] = self.parse_user_tracks(video['tracklist'])
        return ret

    def parse_user_tracks(self, tracks: list) -> list:
        ret = list()
        for i in range(0, len(tracks) - 1):
            tmp_track = dict()
            tmp_track['name'] = tracks[i]['name']
            tmp_track['start'] = tracks[i]['start']
            tmp_track['duration'] = self.calc_duration(
                tmp_track['start'],
                tracks[i + 1]['start'])
            ret.append(tmp_track)

        tmp_track = dict()
        last_index = len(tracks) - 1
        tmp_track['name'] = tracks[last_index]['name']
        tmp_track['start'] = tracks[last_index]['start']
        tmp_track['duration'] = None
        ret.append(tmp_track)
        return ret

    def parse_input(self, data: list):
        """Parse input to output format (see module docstring for info)"""
        ret = list()
        for video in data:
            data = self.parse_video(video)
            if data is None:
                return None
            ret.append(data)
        return ret

    def get_video_info(self, url: str) -> dict:
        """Get info about video"""
        ytdl = youtube_dl.YoutubeDL(self.ytdl_options)
        return ytdl.extract_info(url)

    def get_filename(self, video_info) -> str:
        """Get filename of youtube_dl output file"""
        ytdl = youtube_dl.YoutubeDL(self.ytdl_options)
        return ytdl.prepare_filename(video_info)

    @staticmethod
    def get_video_name(video_info) -> str:
        return video_info['title']

    @staticmethod
    def get_track_list(video_info):
        if 'chapters' not in video_info:
            return None
        else:
            return video_info['chapters']

    @staticmethod
    def parse_tracks_from_video(tracklist):
        ret = list()
        for track in tracklist:
            t = dict()
            t['name'] = clean_filename(track['title'])
            t['start'] = str(track['start_time'])
            t['duration'] = str(track['end_time'] - track['start_time'])
            ret.append(t)

        return ret

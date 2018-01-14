"""Data parser for the cutter"""
from datetime import datetime
import youtube_dl


class InputParser(object):
    def __init__(self):
        self.ytdl_options = {'format': 'bestaudio/best', 'quiet': True, 'simulate': True}

    @staticmethod
    def calc_duration(start: str, end: str) -> str:
        try:
            time_format = "%M:%S"
            delta = datetime.strptime(end, time_format) - datetime.strptime(start, time_format)
        except ValueError:
            time_format = "%H:%M:%S"
            delta = datetime.strptime(end, time_format) - datetime.strptime(start, time_format)
        
        return str(delta)

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
            t['name'] = track['title']
            t['start'] = str(track['start_time'])
            t['duration'] = str(track['end_time'] - track['start_time'])
            ret.append(t)

        return ret

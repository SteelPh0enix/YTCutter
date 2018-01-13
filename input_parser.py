"""Data parser for the cutter"""
from datetime import datetime, timedelta
import youtube_dl


class InputParser(object):
    def __init__(self):
        pass

    @staticmethod
    def calc_duration(start: str, end: str) -> str:
        try:
            time_format = "%M:%S"
            delta = datetime.strptime(end, time_format) - datetime.strptime(start, time_format)
        except ValueError:
            time_format = "%H:%M:%S"
            delta = datetime.strptime(end, time_format) - datetime.strptime(start, time_format)
        
        return str(delta)

    def parse_video(self, video: dict) -> dict:
        ret = dict()
        ret['url'] = video['url']
        ret['filename'] = self.get_filename(video['url'])
        ret['output_dir'] = ret['filename'].rsplit('-', 1)[0]
        ret['tracklist'] = self.parse_tracks(video['tracklist'])
        return ret

    def parse_tracks(self, tracks: list) -> list:
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

    def parse_input(self, data: list) -> list:
        """Parse input to output format (see module docstring for info)"""
        ret = list()
        for video in data:
            ret.append(self.parse_video(video))
        return ret

    @staticmethod
    def get_filename(url: str) -> str:
        """Get filename for output file. Not very efficient. Maybe will change later."""
        ytdl = youtube_dl.YoutubeDL({'quiet': True, 'simulate': True})
        result = ytdl.extract_info(url)
        return ytdl.prepare_filename(result)

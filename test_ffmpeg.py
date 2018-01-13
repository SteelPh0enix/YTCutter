import os.path
import unittest
import ffmpeg
import youtube_dl


class TestFFmpeg(unittest.TestCase):
    def download_file(self):
        with youtube_dl.YoutubeDL(self.ydl_options) as downloader:
            return downloader.download([self.video])

    def setUp(self):
        self.ydl_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus'
            }],
        }
        self.video = 'https://www.youtube.com/watch?v=ldwg3eXiISM'
        self.video_name = 'ALEX & Tokyo Rose - AKUMA [Full Album] 2017-ldwg3eXiISM.opus'
        if not os.path.isfile(self.video_name):
            self.download_file()

    def test_cut(self):
        filename = self.video_name
        output = 'test.opus'
        start = '00:10:20'
        duration = '00:20:30'

        ff = ffmpeg.FFmpeg()
        ret = ff.extract_opus(filename, start, duration, output)
        self.assertEqual(ret.returncode, 0)
        os.remove(output)

    def test_cut_no_duration(self):
        filename = self.video_name
        output = 'test.opus'
        start = '00:10:20'

        ff = ffmpeg.FFmpeg()
        ret = ff.extract_opus(filename, start, None, output)
        self.assertEqual(ret.returncode, 0)
        os.remove(output)


if __name__ == '__main__':
    unittest.main()

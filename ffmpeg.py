"""Basic FFmpeg wrapping functions"""
import subprocess


class FFmpeg(object):
    def __init__(self):
        self.ffmpeg = 'ffmpeg'

    def extract_opus(self, filename: str, start: str,
                     duration, output_file: str) -> subprocess.CompletedProcess:
        """Extract audio in OPUS format from file"""
        args = [self.ffmpeg, '-i', filename, '-ss',
                start]
        if duration is not None:
            args += ['-t', duration]

        args += ['-c', 'copy', output_file]
        return subprocess.run(args, stdout=subprocess.PIPE)

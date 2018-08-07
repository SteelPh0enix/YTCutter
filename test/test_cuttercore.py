import unittest
import cuttercore
import os
import glob

class TestCutterCore(unittest.TestCase):
    def test_download_video(self):
        video_url = "https://www.youtube.com/watch?v=_xoxUEKb0os"
        expected_dir = "./Carpenter Brut - Leather Teeth [Full Album]"
        expected_tracks = [
            "Leather Teeth",
            "Cheerleader Effect",
            "Sunday Lunch",
            "Monday Hunt",
            "Inferno Galore",
            "Beware The Beast",
            "Hairspray Hurricane",
            "End Titles"
        ]
        
        cutter = cuttercore.CutterCore()
        cutter.download_video(video_url, False)

        # check directory structure
        self.assertTrue(os.path.isdir(expected_dir), "Directory with tracks not found!")
        for track in expected_tracks:
            file_count = len(glob.glob(expected_dir + '/' + track + '.*'))
            self.assertNotEqual(file_count, 0, "Didn't found track '{0}'!".format(track))
            self.assertEqual(file_count, 1, "There's more than one track '{0}' (probably different extensions, shouldn't happen)!".format(track))
    
    def test_parse_file(self):
        pass

if __name__ == '__main__':
    unittest.main()
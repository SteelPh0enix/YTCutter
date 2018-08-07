import argparse
import cuttercore

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage="%(prog)s youtube video links (downloads all the videos basing on tracklists inside description)\n"
        "or\n"
        "%(prog)s -f file.json (downloads videos according to file structure)",
        epilog="just don't forget to buy the stuff you download, be kind to creators")
    parser.add_argument("-f", "--file", help="Use JSON file instead of YouTube link(s)", action="store_true")
    parser.add_argument("-d", "--no-delete-original", help="Keep original, uncutted audio/video file", action="store_false", dest="nodelete")
    parser.add_argument("videos", help="Link(s) to YouTube video or path to JSON file", type=str, nargs="+")
    args = parser.parse_args()
        
    cutter = cuttercore.CutterCore()

    if args.file:
        cutter.parse_files(args.videos, args.nodelete)
    else:
        cutter.download_videos(args.videos, args.nodelete)

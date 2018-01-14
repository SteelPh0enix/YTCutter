"""Entry point"""
import json
import sys
from ytcutter_core import YTCutter, CouldNotReadTracksException

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("USAGE:\nPass an URL as argument or \'-f [filename]\' to read input from file.")
        sys.exit(1)

    if sys.argv[1] == '-f':
        with open(sys.argv[2], 'r') as f:
            data = json.load(f)
    else:
        data = [{'url': sys.argv[1]}]

    cutter = YTCutter()
    try:
        cutter.run(data)
    except CouldNotReadTracksException:
        print("Cutter couldn't automatically recognize tracklist. Put tracklist in input JSON file and try again.")
        sys.exit(2)

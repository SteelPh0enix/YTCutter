"""Entry point"""
import json
import sys
from ytcutter import YTCutter

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("USAGE: python . [JSON file with input data")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        data = json.load(f)

    YTCutter().run(data)
"""Entry point"""
import json
from ytcutter import YTCutter

if __name__ == '__main__':
    data = json.load(open('input.json'))

    YTCutter().run(data)
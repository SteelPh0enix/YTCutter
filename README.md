# YTCutter
YouTube video downloading&amp;cutting tool

This script can be used for downloading and automatically splitting music albums uploaded to YouTube.
It can get the tracklist from video's metadata, or you can pass the tracklist as JSON file.

## Installation
Just install youtube_dl using pip and clone this repo.
And make sure you have FFmpeg downloaded and in PATH.

To make your own executable, install cx_Freeze and run `python setup.py build`

## Usage
``ytcutter.exe [video url]``.
And the cutter will try to get tracklist from video metadata and download&cut it.

Or, you can pass JSON file path as argument for script. For example `ytcutter.exe -f input.json`

Input should look like that:
```
[{
    'url': 'url of the video',
    'tracklist': [{
        'start': '00:00:00.000', (HH:MM:SS.MS format, can be shorted to HH:MM:SS or MM:SS, or just seconds. Must be a string.)
        'name': 'Track name'
    }, { another track }]
}, { another video }]
```

You can ommit tracklist, because some of the videos has the tracklist in metadata.
Cutter will try to use it, or will return an error if it will be unable to.
After that, you should get your video cutted to tracks in a video title directory.

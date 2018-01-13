# YTCutter
YouTube video downloading&amp;cutting tool

## Info

For now, it works only for OPUS files. This means, if your video isn't available in OPUS format, the cutter will either fail or cut your files and leave them with .opus extension. This will be fixed.

## Installation
Just install youtube_dl using pip and clone the repo.
And make sure you have FFmpeg downloaded and in PATH.

## Usage
Pass JSON file path as argument for script. For example `python . input.json`

Input should look like that:
```
[{
    'url': 'url of the video',
    'tracklist': [{
        'start': '00:00:00.000', (HH:MM:SS.MS format, can be shorted to HH:MM:SS or MM:SS, or just seconds (probably))
        'name': 'Track name'
    }, { another track }]
}, { another video }]
```

# YTCutter
YouTube video downloading&amp;cutting tool

## Info

For now, it works only for OPUS files. This means, if your video isn't available in OPUS format, the cutter will either fail or cut your files and leave them with .opus extension. This will be fixed.

## Installation
Just install youtube_dl using pip and clone the repo.

## Usage
Put the list of videos with track information in `input.json` and run `python .` in directory with Cutter `__main__.py` file.
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

Will make some adjustments to that.

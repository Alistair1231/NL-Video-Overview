# Northernlion Channel Scraper / Playlist Generator
This is a collection of commands / documentation to scrape the Northernlion channel for videos and generate playlists for specific games.

This also contains the scraped data for anyone to access and save people from the need to scrape over 20k videos before starting to use it. 

It is set up in a way that should make it easy to update the data when new videos are uploaded.

## Getting started
To use this, install jq and yt-dlp e.g. using `scoop` on windows, `brew` on mac and `nix` on linux.  

## Setting up add-to-playlist
If you want to automatically create playlists follow these steps, otherwise you can skip this section.

First install python, the version shouldn't matter, but it can be beneficial to lag a version behind the latest. So if the latest is 3.10, install 3.9.

Also you need to create a project in the [Google Cloud Console](https://console.cloud.google.com/) and enable the YouTube Data API v3 in it, then create OAuth 2.0 credentials (client ID and client secret) for a desktop application. Copy `yt.env.example` to `yt.env` and fill in the values.

The script doesn't have many dependencies, you can install them with `pip install -r requirements.txt`. 

## Usage

### Generate yt-urls.txt
so that you can cancel/resume without rescraping the channel
```bash
yt-dlp --flat-playlist -i --print-to-file url intermediary/yt-urls.txt https://www.youtube.com/@Northernlion
```


### gather up video info into json
- the cookies-from-browser flag helps a lot with rate limiting, you need to be logged in and replace brave with your browser
- the replace-in-metadata flag is used to replace quotes with single-quotes, to avoid issues with the json format
- print-to-file is used to save the info in json format
- download-archive / force-write-archive is used to track which videos have been processed already
```bash
yt-dlp --simulate --verbose --batch-file intermediary/yt-urls.txt --cookies-from-browser brave --download-archive intermediary/done.txt --force-write-archive --replace-in-metadata "title,channel" "\"" "'" --print-to-file '{"channel": "%(channel)s", "uploadDate": "%(upload_date)s", "videoUrl": "%(webpage_url)s", "title": "%(title)s"}' intermediary/nl.json
```

### filter out a game from list of videos 
- be aware that this is case sensitive, so Climbing is not the same as climbing
- Replace `(A Difficult Game About Climbing)` with what you want to search for
```bash
jq -s '[.[] | select(.title | contains("(A Difficult Game About Climbing)"))] | sort_by(.uploadDate)' intermediary/nl.json > games/climbing-game.json
```
**manually validate the list**
```bash
vim games/climbing-game.json
```

### generate a list of urls for the playlist-adder
```bash
jq -r '.[].videoUrl' games/climbing-game.json > games/climbing-game-urls.txt
```
### add to playlist

```bash
python add_to_playlist.py --title "Climbing Game - NL" --description "Chronological list of videos for \"Climbing Game\" from Northernlion (NL)" --file games/climbing-game-urls.txt

```


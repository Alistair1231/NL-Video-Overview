# Northernlion Channel Scraper / Playlist Generator
This is a collection of commands / documentation to scrape the Northernlion channel for videos and generate playlists for specific games.

This also contains the scraped data for anyone to access and save people from the need to scrape over 20k videos before starting to use it. 

It is set up in a way that should make it easy to update the data when new videos are uploaded.

## Getting started
To use this, install jq and yt-dlp e.g. using `scoop` on windows, `brew` on mac and `nix` on linux.  

## Usage

### Generate yt-urls.txt
so that you can cancel/resume without rescraping the channel
```bash
rm intermediary/yt-urls.txt
yt-dlp \
  --flat-playlist \
  --ignore-errors \
  --print-to-file 'url' intermediary/yt-urls.txt \
  https://www.youtube.com/@Northernlion
```


### gather up video info into json
- the cookies-from-browser flag helps a lot with rate limiting, you need to be logged in and replace brave with your browser
- the replace-in-metadata flag is used to replace quotes with single-quotes, to avoid issues with the json format
- print-to-file is used to save the info in json format
- download-archive / force-write-archive is used to track which videos have been processed already
```bash
yt-dlp \
  --simulate \
  --verbose \
  --batch-file intermediary/yt-urls.txt \
  --cookies-from-browser brave \
  --download-archive intermediary/done.txt \
  --force-write-archive \
  --replace-in-metadata "title,channel" "\"" "'" \
  --print-to-file '{"channel": "%(channel)s", "uploadDate": "%(upload_date)sT%(epoch-3600>%H%M%S)s", "videoUrl": "%(webpage_url)s", "title": "%(title)s"}' \
  intermediary/nl.json
```

### filter out a game from list of videos 
- be aware that this is case sensitive, so Climbing is not the same as climbing
- Replace `(A Difficult Game About Climbing)` with what you want to search for
```bash
jq -s '[.[] | select(.title | contains("(A Difficult Game About Climbing)"))] | sort_by(.uploadDate)' \
  intermediary/nl.json > games/climbing-game.json
```
**manually validate the list**
```bash
code games/climbing-game.json
```

### generate a list of urls for the playlist-adder
```bash
jq -r '.[].videoUrl' \
  games/climbing-game.json > games/climbing-game-urls.txt
```
### add to playlist

To add the videos to a playlist, I do 50 at a time (limit of anonymous playlists).  
I first create an anonymous playlist and then use the 3$ Patreon-only feature of PocketTube to add the videos to the playlist all at once.

To split the list of urls into 50 per file, you can use the following command. We want the coreutils version of split, because the mac version does not support the --additional-suffix flag, and the youtube playlist generator needs a .txt extension for the "import" feature (CMD-I on Mac)
```bash
split -l 50 games/balatro-urls.txt games/balatro-urls- --additional-suffix=.txt
# on mac: brew install coreutils and use gsplit
gsplit -l 50 games/balatro-urls.txt games/balatro-urls- --additional-suffix=.txt
# on windows your alone on this one, I would just use msys/cygwin or wsl instead of fighting with powershell, but you do you)
```

To create the anonymous playlist, you can use the following:
- Use this downloadable tool: [christianhofmanncodes/youtube-playlist-generator](https://github.com/christianhofmanncodes/youtube-playlist-generator)
- or this website: https://apps.dominiczelek.com/youtube-playlist-from-links/

[PocketTube](https://pockettube.io/) has a Patreon-only feature that allows you to add all videos in a list to another playlist at once. We do this to have the 5000 video limit of a playlist instead of the 50 video limit of an anonymous playlist, also you cannot save anonymous playlists.
At the time of writing the UI of PocketTube looks like this:

![add-to-playlist](add-to-playlist.png)

--- 
I did create a semi-working python script for this but decided against refining it, the last commit with it is [5343200](https://github.com/Alistair1231/NL-Video-Overview/commit/5343200dc2ee1542d06d4fcda916b62c2f607aa4), feel free to use it as a starting point and create a PR if you want to improve it and provide a free alternative to the Patreon-only feature of PocketTube. This still doesn't get around the 200 per-day limit of the youtube api, but that's not that big of a deal imo.

## Summary
```bash
jq -s '[.[] | select(.title | contains("(A Difficult Game About Climbing)"))] | sort_by(.uploadDate)' intermediary/nl.json > games/climbing-game.json

code games/climbing-game.json

jq -r '.[].videoUrl' games/climbing-game.json > games/climbing-game-urls.txt

code games/climbing-game-urls.txt
```
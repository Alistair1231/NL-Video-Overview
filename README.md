## Getting started
To use this, install jq and yt-dlp e.g. using `scoop` on windows, `brew` on mac and `nix` on linux.  

## Setting up add-to-playlist
If you want to automatically create playlists follow these steps:

You need to create a project in the [Google Cloud Console](https://console.cloud.google.com/) and enable the YouTube Data API v3 in it, then create OAuth 2.0 credentials (client ID and client secret) for a desktop application. Copy `yt.env.example` to `yt.env` and fill in the values.

The script doesn't have many dependencies, you can install them with `pip install -r requirements.txt`. 

Example usage:
```bash
# Generate yt-urls.txt, so that you can cancel/resume without rescraping the channel
yt-dlp --flat-playlist -i --print-to-file url intermediary/yt-urls.txt https://www.youtube.com/@Northernlion

# gather up info about videos and save in json format
## the cookies-from-browser flag helps a lot with rate limiting, you need to be logged in and replace brave with your browser
## the replace-in-metadata flag is used to replace quotes with single-quotes, to avoid issues with the json format
yt-dlp --simulate --verbose --batch-file intermediary/yt-urls.txt --cookies-from-browser brave --download-archive intermediary/done.txt --force-write-archive --replace-in-metadata "title,channel" "\"" "'" --print-to-file '{"channel": "%(channel)s", "uploadDate": "%(upload_date)s", "videoUrl": "%(webpage_url)s", "title": "%(title)s"}' intermediary/nl.json

# filter out a game from list of videos (be aware that this is case sensitive, so Climbing is not the same as climbing)
jq -s '[.[] | select(.title | contains("(A Difficult Game About Climbing)"))] | sort_by(.uploadDate)' intermediary/nl.json > games/climbing-game.json

# ! manually validate the list
vim games/climbing-game.json

# create url list for playlist-adder
jq -r '.[].videoUrl' games/climbing-game.json > games/climbing-game-urls.txt

# add to playlist
python add_to_playlist.py --title "Climbing Game - NL" --description "Chronological list of videos for \"Climbing Game\" from Northernlion (NL)" --file games/climbing-game-urls.txt

```


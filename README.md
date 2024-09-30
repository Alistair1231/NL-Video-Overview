To use this, install jq, sed and yt-dlp e.g. using `scoop` on windows, `brew` on mac and `nix` on linux.  
For adding to your accounts playlist, you also need python and these packages: `pip install google-auth-oauthlib google-api-python-client`

```bash
# Generate yt-urls.txt
yt-dlp --flat-playlist -i --print-to-file url yt-urls.txt https://www.youtube.com/@Northernlion

# prepare json file, by removing the bracket and adding a comma on the last line
sed -i '$s/]$/,/' nl.json

# gather up info about videos and save in json format
yt-dlp --simulate --verbose --batch-file yt-urls.txt --cookies-from-browser brave --download-archive done.txt --force-write-archive --replace-in-metadata "title,channel" "\"" "'" --print-to-file '{"channel": "%(channel)s", "uploadDate": "%(upload_date)s", "videoUrl": "%(webpage_url)s", "title": "%(title)s"}' nl.json

# filter out a game from list of videos
jq -sc '[.[] | select(.title | contains("Climbing"))] | sort_by(.uploadDate)' nl.json > games/climbing-game.json

# ! manually validate the list

# create url list for playlist-adder
jq -r '.[].videoUrl' games/climbing-game.json > games/climbing-game-urls.txt

# add to playlist
python add_to_playlist.py --title "Climbing Game - NL" --description "Chronological list of videos for \"Climbing Game\" from Northernlion (NL)" --file games/climbing-game-urls.txt

```
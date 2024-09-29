To use this, install jq and yt-dlp e.g. using `scoop` on windows, `brew` on mac and `nix` on linux.  
For adding to your accounts playlist, you also need python and these packages: `pip install google-auth-oauthlib google-api-python-client`

```bash
# Generate yt-urls.txt
yt-dlp --flat-playlist -i --print-to-file url yt-urls.txt https://www.youtube.com/@Northernlion

# gather up json output format
yt-dlp --simulate --verbose --batch-file yt-urls.txt --cookies-from-browser brave --download-archive done.txt --force-write-archive --replace-in-metadata "title,channel" "\"" "'" --print-to-file '{"channel": "%(channel)s", "uploadDate": "%(upload_date)s", "videoUrl": "%(webpage_url)s", "title": "%(title)s"},' nl.json

# ! manually edit the last line to remove the trailing comma and add the closing bracket

# filter out a game
jq '[.[] | select(.title | contains("Climbing"))] | sort_by(.uploadDate)' nl.json > games/climbing-game.json

# create url list for playlist-adder
jq -r '.[].videoUrl' games/climbing-game.json > games/climbing-game-urls.txt

# add to playlist
python add_to_playlist.py --title "Climbing Game - NL" --description "Chronological list of videos for \"Climbing Game\" from Northernlion (NL)" --file games/climbing-game-urls.txt

``


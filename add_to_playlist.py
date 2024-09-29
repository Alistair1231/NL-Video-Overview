import os
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def get_authenticated_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('youtube', 'v3', credentials=creds)

def get_or_create_playlist(youtube, title, description):
    # Check if playlist already exists
    request = youtube.playlists().list(
        part="snippet",
        mine=True
    )
    response = request.execute()

    for item in response['items']:
        if item['snippet']['title'] == title:
            print(f"Playlist '{title}' already exists. Using existing playlist.")
            return item['id']

    # If playlist doesn't exist, create it
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": title,
            "description": description
          },
          "status": {
            "privacyStatus": "private"
          }
        }
    )
    response = request.execute()
    print(f"Created new playlist '{title}'")
    return response['id']

def add_video_to_playlist(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    request.execute()

def extract_video_id(url):
    if "youtu.be" in url:
        return url.split("/")[-1]
    elif "youtube.com" in url:
        return url.split("v=")[1].split("&")[0]
    else:
        return None

def main(title, description, file_path):
    youtube = get_authenticated_service()
    
    playlist_id = get_or_create_playlist(youtube, title, description)
    print(f"Using playlist with ID: {playlist_id}")
    
    try:
        with open(file_path, 'r') as file:
            video_urls = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except IOError:
        print(f"Error: There was an issue reading the file {file_path}.")
        return

    for url in video_urls:
        url = url.strip()  # Remove any leading/trailing whitespace
        video_id = extract_video_id(url)
        if video_id:
            try:
                add_video_to_playlist(youtube, playlist_id, video_id)
                print(f"Added video {video_id} to playlist")
            except Exception as e:
                print(f"Error adding video {video_id}: {str(e)}")
        else:
            print(f"Invalid YouTube URL: {url}")
    
    print("Playlist update complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create or update a YouTube playlist from a list of URLs in a text file.')
    parser.add_argument('--title', required=True, help='Title of the playlist')
    parser.add_argument('--description', required=True, help='Description of the playlist')
    parser.add_argument('--file', required=True, help='Path to the text file containing YouTube URLs')
    
    args = parser.parse_args()
    
    main(args.title, args.description, args.file)
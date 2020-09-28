import re
import urllib.request
import math
from bs4 import BeautifulSoup
from datetime import date
import requests
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def getVideoIds(url):
    linkcollection = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    print("A")
    for post in soup.find_all("blockquote"):
        #regex expression to find youtube links in the post text, works on videos with an 11 character id which is all at the moment but this is subject to change.
        links = re.findall(r"(?:http(?:s?):\/\/(?:www\.)?(?:m\.)?youtu(?:be\.com\/(?:watch\?(?:\&)?v=|embed\/)|\.be\/))(?P<video_id>[\w\-\_]{11})(?:&(amp;)?​[\w\?‌​=]*)?",post.text)
        if links:
            for eachlink in links:
                #for some reason the regex returns a tuple with a empty second value, perhaps this is due to Group0 being returned would like to know why this happens, this quickfix only takes the ID
                linkcollection.append(eachlink[0])


    print("There Are :"+str(len(linkcollection))+" Videos in the Thread")
    return linkcollection



def createPlaylist(youtube):
    today = date.today()
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
            "title": ("Bleep " + today.strftime("%m/%d/%y")),
            "description":("Bleep Playlist for "+today.strftime("%m/%d/%y")),
            "tags": [
            "Electronic Music",
            ],
            "defaultLanguage": "en"
             },
             "status": {
            "privacyStatus": "public"
             }
        }
    )
    response = request.execute()
    return response["id"]

def addVideosToPlaylist(youtube,newVideos,playlistId):
    for video in newVideos:
        request = youtube.playlistItems().insert(
            part="snippet",
                body={
                    "snippet": {
                    "playlistId": playlistId,
                    "position": 0, #this results in the playlist being backwards in regards to post order
                    "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video
                                }
                            }
                    }
        )
        response = request.execute()



def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR CLIENT SECRETS FILE LOCATION"
    DEVELOPER_KEY = "YOUR DEVELOPER KEY"
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    url = input("Post Url of current Bleep Thread")
    newvideos = getVideoIds(url)
    playlistId = createPlaylist(youtube)
    addVideosToPlaylist(youtube,newvideos,playlistId)
    print("All videos added to playlist")



if __name__ == "__main__":
    main()

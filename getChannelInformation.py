import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
youtube = build('youtube' , 'v3', developerKey= API_KEY )


def get_channel_id(channel_url):
    response = requests.get(channel_url)
    if response.status_code == 200:
        page_source = response.text
        soup = BeautifulSoup(page_source, 'html.parser')
        for script in soup.find_all('script'):
            if 'channelId' in script.text:
                start = script.text.find('"channelId":"') + len('"channelId":"')
                end = script.text.find('"', start)
                channel_id = script.text[start:end]
                if channel_id:
                    return channel_id
    return None

def get_channel_detial(channel_id, base_url):
    url = f"{base_url}/channels?part=snippet,contentDetails,statistics&id={channel_id}&key={API_KEY}"
    response = requests.get(url)
    try:
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decode error occurred: {json_err}")
        print(f"Response content: {response.content}")
    return None
    

def get_video_ids(channel_id):
    video_ids = []
    next_page_token = None

    while True:
        requests = youtube.search().list(
            part = 'id',
            channelId = channel_id,
            maxResults = 100,
            order = 'date',
            pageToken = next_page_token
        )

        response = requests.execute()


        for item in response['items']:
            if 'videoId' in item['id']:
                video_ids.append(item['id']['videoId'])
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
            
    return video_ids

def get_video_details(video_ids):
    video_data = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()
        
        for video in response['items']:
            video_data.append({
                'video_id': video['id'],
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'published_at': video['snippet']['publishedAt'],
                'view_count': int(video['statistics'].get('viewCount', 0)),
                'like_count': int(video['statistics'].get('likeCount', 0)),
                'comment_count': int(video['statistics'].get('commentCount', 0)),
                'duration': video['contentDetails']['duration']
            })
    
    return pd.DataFrame(video_data)



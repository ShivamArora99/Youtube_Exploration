import requests
import json
import pandas as pd
import getChannelInformation

BASE_URL = 'https://www.googleapis.com/youtube/v3'
channel_url = 'https://www.youtube.com/@cokestudio'

# get channel id:
CHANNEL_ID = getChannelInformation.get_channel_id(channel_url)

if CHANNEL_ID:
    print(f"Channel ID: {CHANNEL_ID}")
else:
    print("Channel ID not found.")

# get channel details:

channel_details = getChannelInformation.get_channel_detial(channel_id= CHANNEL_ID , base_url= BASE_URL)

if channel_details:
    print(json.dumps(channel_details , indent= 4))
else:
    print("Failed to retrieve channel details")


video_ids = getChannelInformation.get_video_ids(CHANNEL_ID)
print(video_ids)
if video_ids:
        print(f"Retrieved {len(video_ids)} video IDs.")
        video_details_df = getChannelInformation.get_video_details(video_ids)
        video_details_df.to_csv('youtube_video_details.csv', index=False)
        print("Video details saved to youtube_video_details.csv")
else:
        print("No videos found for the channel.")



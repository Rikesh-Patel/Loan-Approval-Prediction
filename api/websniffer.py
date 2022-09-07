# Call libraries required
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


# Set vars specific to WebSnifferHQ YT Channel
api_key = 'AIzaSyBRBZNTrA1yVwLM99jM-SvVEKkdIJG_UKw'
channel_ids = ['UCHtLNbdagCIfir1ulloAEhQ']
youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_stats(youtube, channel_ids):
    all_data = []
    # Request channel statistics from API
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id=','.join(channel_ids))
    response = request.execute() 
    # Get key values from channel data response
    for i in range(len(response['items'])):
        data = dict(channel_name = response['items'][i]['snippet']['title'],
                    subscribers = response['items'][i]['statistics']['subscriberCount'],
                    views = response['items'][i]['statistics']['viewCount'],
                    total_videos = response['items'][i]['statistics']['videoCount'],
                    playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    
    return all_data, response

# Call function and format dataframe
channel_statistics, response = get_channel_stats(youtube, channel_ids)
channel_data = pd.DataFrame(channel_statistics)
channel_data['subscribers'] = pd.to_numeric(channel_data['subscribers'])
channel_data['views'] = pd.to_numeric(channel_data['views'])
channel_data['total_videos'] = pd.to_numeric(channel_data['total_videos'])
channel_data['refresh_date'] = datetime.today().strftime('%m/%d/%Y')

playlist_id = channel_data.loc[channel_data['channel_name']=='WebSniffer', 'playlist_id'].iloc[0]

# Function to get complete list of all videos published by WebSnifferHQ 
def get_video_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = playlist_id,
                maxResults = 50)
    response = request.execute()
    
    video_ids = []
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    more_pages = True
    
    # If more than 50 results on first page, then iterate to next page
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId = playlist_id,
                        maxResults = 50,
                        pageToken = next_page_token)
            response = request.execute()
    
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            next_page_token = response.get('nextPageToken')
        
    return video_ids

video_ids = get_video_ids(youtube, playlist_id)

# Function to get statistics on all videos created by WebSnifferHQ
def get_video_details(youtube, video_ids):
    all_video_stats = []
    for i in range(0, len(video_ids), 50):
        # Get list of all ids of WebSnifferHQ Videos
        request = youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(video_ids[i:i+50]))
        response = request.execute()

        # Create table of statistics with each video from list of published videos
        for video in response['items']:
            video_stats = dict(Title = video['snippet']['title'],
                               Published_date = video['snippet']['publishedAt'],
                               Views = video['statistics']['viewCount'],
                               Likes = video['statistics']['likeCount'],
                               Comments = video['statistics']['commentCount'],
                               ID = video['id']
                               )
            all_video_stats.append(video_stats)
    
    return all_video_stats

# Clean up video_details dataframe
video_details = get_video_details(youtube, video_ids)
video_data = pd.DataFrame(video_details)
video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Comments'] = pd.to_numeric(video_data['Comments'])

# Append missing statisics to channel_data table
channel_data['likes'] = video_data['Likes'].sum()
channel_data['comments'] = video_data['Comments'].sum()
channel_data['last_published'] = video_data['Published_date'].max()


# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
json_dict = {"type": "service_account", "project_id": "divine-bonbon-353604", "private_key_id": "acc822a3ff0033b804e5b3bd877ffe4397fa0c9a", "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQChUDY+RMQg8o8D\nSm8IHx4BA/hvIaasEkebOKxzHL7iGi/l0P3+9xmWu18JazNCb8uesrBlHceeTiZ4\nJOmSaDhj3+EwU7CuJP/1q7J64wt8VEtQnSk8XaD9Sbux2wWqaaSzSHp+GckPv62P\n2k8pRkCPKqiWnIeP2rNp0hJMBBeU7wye5AFhp0KRJOuIqjmTj7a7BLemQdRT0jWr\npK2iixUt4ulz+jAaZ9eMfJoSu/PSQKw+3tW7dfDxvx2cx9ayFONoTRpFsLDQe/L/\neD8n0PGvj9dM8a7hZWhkqjIvYEIx/mYs6OEwAyFxedu4rz1svwFgHkn+v0hFcOUl\nIWFN64lhAgMBAAECggEAAJQMHDiAJCc7y2/Zupb0uf5s1+N73OtmqQHJdw8bRChI\ncdnEWPsasCBzDs6ivdZMADxo46+cGI+qmFgprzgW//88/k1XS2v8VMqsc2hax4YW\npHkifilI0IZQWq/CjN4uFN5DaYVnRd1fxMjMMx6rbY7/Tu8CnKHyxX5KluMy8aQH\nq+pdEmnePZPVfRfAFKwK+DEF8ACCZZL8IYs0dtjRDH8Km0HuVpcGvhFF5yAzn0mZ\naEyj5buOliQd1eb0kipWt9N2lm2MQcRZQQhppMhF99+tWAw62vVECIPPi91a1tcz\ndibiOdjhYU44rIXhIfiH8ubEIWO/dMkx1frPoir5yQKBgQDZNFGmETwL9/9sdXzG\nsy0TYOq3znObCq36d2WqrfDyr5q+xqd40xSnUCJWblBFxQDvS3M7CrnRm2I6Rlli\nF4+/AGoNQpKWYhfNo3rjPfGhv/cpJCcXjYDakGqoSLPD4lme1m3ij++OibRqv4dm\n4Hss8nYsjbOdvxRoPZe+sFSPqQKBgQC+IEWpYEInGhlkuVTXAEtjSy95IJsgoi75\nSBQpgEAotvdQTRwEOX5aIM6aIJPsL8zd84Vob3NQFTuLeBLJLe2ApLCdfTPAXsyO\n/0AsHkNY+J8AVc4aCN9I5DrIjiyCMT1orMOLT4AIj2EOaa0Tw+hK7+Jl62CZZ8iG\nouPk6eYe+QKBgGrGPnENveAAXO8bXmhrgngpR5luAwSvnlEnSrI56d3Tl5W7IG7U\nDS4mxYqJliqGKux3wcC/iBNTeFk/ZgdDn+V8NaYpGNiWhi8P84QsWlFyhfUSkakR\nZcuL/PKXMs/TwMzFiqU6rr/6T9e+KbjYF5VD5/YE/sxIN6b6yFL0ac1pAoGBAK8z\nPf5e3Zb6zfurbSrS8qWFWzHbghgIXBELAslbjcP3Ft/ArtiVwoF7SedtreIwCjFd\nfspGKZTafAyBkY4h7IJnQPlfrpjOwuHjBVeia51JPfwpFcuX8WpSJnk5ynoOtfAH\nhAqUL/+zYFTPvNZB6YVkmNQimtnCcV7gK/F+OLjBAoGADf/8rAMBw4LB9DL8V3b2\nANxVxInQkT8yZbyasDIph0lL0pKn8yoHMKwOrJadKhK62iMw/+L4+zGwmwLZM6Zq\nOZIEY5WI+mcB/wEPn9bTmDtkJCvxXwwFxEQ0uGuShax8Ckm8nXDwsEKOxFXWQIwo\nDDEbXclAmn9cCYccAGTWExE=\n-----END PRIVATE KEY-----\n", "client_email": "service@divine-bonbon-353604.iam.gserviceaccount.com", "client_id": "104890271830023098765", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service%40divine-bonbon-353604.iam.gserviceaccount.com"}
with open('creds.json', 'w') as f:
  json.dump(json_dict,f)
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('WebSniffer YT Automatic Data')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)
channel_data['last_published'] = channel_data['last_published'].apply(lambda x: x.strftime("%m/%d/%Y"))
sheet_instance.append_rows(channel_data.values.tolist())
sheet_instance.resize(sheet_instance.row_count+1)
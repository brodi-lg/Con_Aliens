#!/usr/bin/env python
# coding: utf-8


pip install python-dotenv


# In[3]:


from dotenv import load_dotenv


# In[4]:


import os


# In[5]:


import requests


# In[6]:


pip install google-api-python-client


# In[7]:


from googleapiclient.discovery import build


# In[8]:


load_dotenv()


# In[9]:


my_key=os.getenv("API_KEY")


# In[10]:


channel_id = 'UCIFk2uvCNcEmZ77g0ESKLcQ'


# In[11]:


youtube = build('youtube', 'v3', developerKey=my_key) 


# In[12]:


import pandas as pd


# In[13]:


import requests

# YouTube API URL to get channel details including topic details
url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,contentDetails,statistics,topicDetails&id={channel_id}&key={my_key}"

# Make the request and get the response
response = requests.get(url)
channel_data = response.json()

# Extract relevant information
if 'items' in channel_data and len(channel_data['items']) > 0:
    channel_info = channel_data['items'][0]
    
    # Get general channel information
    title = channel_info['snippet']['title']
    description = channel_info['snippet']['description']
    subscriber_count = channel_info['statistics'].get('subscriberCount', 'N/A')
    total_views = channel_info['statistics'].get('viewCount', 'N/A')
    video_count = channel_info['statistics'].get('videoCount', 'N/A')
    
    # Get topic details
    topic_ids = channel_info.get('topicDetails', {}).get('topicIds', [])
    topic_categories = channel_info.get('topicDetails', {}).get('topicCategories', [])
    
    # Display the information
    print(f"Channel Title: {title}")
    print(f"Description: {description}")
    print(f"Subscriber Count: {subscriber_count}")
    print(f"Total Views: {total_views}")
    print(f"Total Videos: {video_count}")
    
    # Display topic details
    print("\nTopic IDs:")
    if topic_ids:
        print(", ".join(topic_ids))
    else:
        print("No topic IDs found.")

    print("\nTopic Categories:")
    if topic_categories:
        print(", ".join(topic_categories))
    else:
        print("No topic categories found.")

else:
    print("No channel data found.")


# In[14]:


# Function to get all videos from a channel
def get_all_channel_videos(channel_id):
    
    request = youtube.channels().list(part='contentDetails',id=channel_id)
    response = request.execute()
    
    # Check if the response contains items
    if 'items' not in response or len(response['items']) == 0:
        print("No videos found for this channel.")
        return []

    upload_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Initialize an empty list to store videos
    all_videos = []

    # Paginate through all videos in the upload playlist
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=upload_playlist_id,
            maxResults=50,  # Maximum allowed by API
            pageToken=next_page_token
        )
        response = request.execute()
        all_videos.extend(response['items'])

        # Check if there's another page of results
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return all_videos

def get_video_details(video_id):
    request = youtube.videos().list(
        part='snippet',
        id=video_id
    )
    response = request.execute()

    # Ensure that there are items in the response and access the snippet
    if 'items' in response and len(response['items']) > 0:
        snippet = response['items'][0]['snippet']
        # Check if the 'statistics' field exists in the response
        statistics = response['items'][0].get('statistics', {})

        # Get relevant statistics
        view_count = statistics.get('viewCount', '0')  # Views
        like_count = statistics.get('likeCount', '0')  # Likes
        tags = snippet.get('tags', [])  # Tags might not be available for every video
       
        return view_count, like_count,tags
    return '0', '0', []


# Function to extract video details and convert to a DataFrame
def videos_to_dataframe(videos):
    # Create a list of dictionaries to store video details
    video_data = []

    for video in videos:
        # Ensure 'snippet' and 'resourceId' exist
        snippet = video.get('snippet', {})
        resource_id = snippet.get('resourceId', {})

        # Get the video ID and title
        video_id = resource_id.get('videoId')
        if not video_id:
            continue  # Skip if video ID is missing

        # Get video details
        view_count, like_count, tags = get_video_details(video_id)


        video_info = {
            'Title': snippet.get('title', 'No Title'),
            'Video ID': video_id,
            'Published At': snippet.get('publishedAt', 'Unknown Date'),
            'View Count': view_count,
            'Like Count': like_count,
            'Tags': ', '.join(tags) if tags else 'No Tags'
        }
        video_data.append(video_info)

    df = pd.DataFrame(video_data)
    return df

# Replace with the actual channel ID you want to investigate
channel_id = 'UCIFk2uvCNcEmZ77g0ESKLcQ' # Example channel ID

# Get all videos from the channel
all_videos = get_all_channel_videos(channel_id)

# Convert to a DataFrame including tags
if all_videos:
    df_videos = videos_to_dataframe(all_videos)
    # Display the DataFrame
    print(df_videos)
else:
    print("No videos retrieved from the channel.")


# In[15]:


pip install isodate


# In[16]:


df_videos.to_csv('channel_videos.csv', index=False)


# In[17]:


df_videos.to_excel('channel_videos.xlsx', index=False)


# In[18]:


#video id 

def get_upload_playlist_id(channel_id):
    request = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    )
    response = request.execute()
    
    if 'items' not in response or len(response['items']) == 0:
        print("Channel not found or has no videos.")
        return None

    # Get the upload playlist ID
    upload_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return upload_playlist_id

# Function to get all video IDs from a playlist
def get_video_ids_from_playlist(playlist_id):
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,  # The maximum number of results per page (50)
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_ids.append(video_id)
        
        # Check if there is another page of results
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return video_ids

# Replace with the actual channel ID you want to investigate
channel_id = 'UCIFk2uvCNcEmZ77g0ESKLcQ'  # Example channel ID

# Get the upload playlist ID for the channel
upload_playlist_id = get_upload_playlist_id(channel_id)

# If the upload playlist ID is found, get the video IDs
if upload_playlist_id:
    video_ids = get_video_ids_from_playlist(upload_playlist_id)
    print(f"Video IDs retrieved: {video_ids}")

    # Optional: Convert the video IDs to a DataFrame for easier viewing or exporting
    df_video_ids = pd.DataFrame(video_ids, columns=['Video ID'])
    print(df_video_ids)
else:
    print("Failed to retrieve video IDs.")


# In[19]:


#since the first extraction did not return view count and like count, i had to try again 
def get_videos_statistics(video_ids):
    video_stats_list = []

    for video_id in video_ids:
        request = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        )
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            video = response['items'][0]
            snippet = video['snippet']
            statistics = video['statistics']

          
            title = snippet['title']
            view_count = statistics.get('viewCount', '0')
            like_count = statistics.get('likeCount', '0')
            comment_count = statistics.get('commentCount', '0')

          
            video_stats_list.append({
                'Video ID': video_id,
                'Title': title,
                'View Count': view_count,
                'Like Count': like_count,
                'Comment Count': comment_count
            })
        else:
            print(f"No data found for video ID: {video_id}")

    return pd.DataFrame(video_stats_list)



df_video_stats = get_videos_statistics(video_ids)


print(df_video_stats)


df_video_stats.to_csv('video_statistics.csv', index=False)


# In[20]:


# Function to get video statistics by video ID
def get_video_statistics(video_id):
    request = youtube.videos().list(
        part='snippet,statistics',  # Include snippet and statistics parts
        id=video_id
    )
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        video = response['items'][0]
        snippet = video['snippet']
        statistics = video['statistics']

        # Extract relevant data
        title = snippet['title']
        view_count = statistics.get('viewCount', '0')
        like_count = statistics.get('likeCount', '0')
        comment_count = statistics.get('commentCount', '0')

        # Print video details
        print(f"Title: {title}")
        print(f"View Count: {view_count}")
        print(f"Like Count: {like_count}")
        print(f"Comment Count: {comment_count}")

        return {
            'title': title,
            'view_count': view_count,
            'like_count': like_count,
            'comment_count': comment_count
        }
    else:
        print(f"No data found for video ID: {video_id}")
        return None


video_id = 'BR_8AxIwKV8'  

# Get video statistics
video_stats = get_video_statistics(video_id)


# In[55]:


df_video_ids.to_csv('channel_video_ids.csv', index=False)


# In[ ]:


#getting videos that are shorts based on duration




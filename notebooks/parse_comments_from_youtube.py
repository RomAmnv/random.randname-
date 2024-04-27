import json
import os
import pandas as pd

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = "AIzaSyDYIns4qLSIahJ5D8zwKspgvBfQk1cZXhU"

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)

videos_id = ["DvsCUI5FNnI", "tihq_bLfk08", "93sKHqxghPU", "oTVsrJrnTC4", "5sG9kmXYsKU", "53CFRYCSGSU", "7c6LQCZt-2s", "_QbbstNuTGI", "NzS52xuLAmI", 
             "VR9EPKz8aXk", "rPp46idEvnM", "47_LhSf-ago", "2I1HnSN1H9o", "x2j_fbTsQo8", "UkwpJyvf8CA", "KdZ4HF1SrFs", "xTpAJWe7ZD4"]
all_comments = []

for video_id in videos_id:

    comments_id_list = youtube.commentThreads().list(videoId=video_id, part="snippet", maxResults=90).execute()

    comments = [comm['snippet']['topLevelComment']['snippet']['textOriginal'] for comm in comments_id_list['items']]
    all_comments += comments
    
data = {"Reviews": all_comments}
df = pd.DataFrame(data)
print(df.head())

df.to_csv("comments_data.csv")
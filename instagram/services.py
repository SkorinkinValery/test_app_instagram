from dotenv import load_dotenv
import os, requests
from typing import List, Dict, Any

load_dotenv()

def get_all_posts() -> List[Dict[str, Any]]:
    '''Получает все посты пользователя из Instagram через Graph API'''

    access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    url = "https://graph.instagram.com/v25.0/me/media"
    params = {
        "fields": "id,media_type,media_url,thumbnail_url,caption,timestamp,permalink,"
                  "like_count,comments_count,shortcode",
        "limit": 50,
        "access_token": access_token
    }

    all_posts: List[Dict[str, Any]] = []
    while url:
        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            raise Exception(data["error"])

        all_posts.extend(data.get("data", []))

        paging = data.get("paging", {})
        url = paging.get("next")
        params = {}

    return all_posts


def add_comment(post_id: str, message: str) -> Dict[str, Any]:
    '''Добавляет комментарий к указанному посту Instagram через Graph API'''

    access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    url = f"https://graph.instagram.com/v25.0/{post_id}/comments"
    data_params = {
        "message": message,
        "access_token": access_token
    }

    response = requests.post(url, data=data_params)
    if response.status_code != 200:
        raise Exception("Instagram API error")
    data = response.json()

    return data
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
import os
import requests

from instagram.models import Post
from instagram.pagination import PostCursorPagination
from instagram.serializers import PostSerializer, CommentSerializer

load_dotenv()

class SyncView(APIView):
    def post(self, request):
        access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')

        url = "https://graph.instagram.com/v25.0/me/media"
        params = {
            "fields": "id,media_type,media_url,thumbnail_url,caption,timestamp,permalink,like_count,comments_count,shortcode",
            "limit": 50,
            "access_token": access_token
        }

        all_posts = []
        while url:
            response = requests.get(url, params=params)
            data = response.json()

            if "error" in data:
                return Response({"error": data["error"]}, status=400)

            all_posts.extend(data.get("data", []))

            paging = data.get("paging", {})
            url = paging.get("next")
            params = {}

        for post in all_posts:
            serializer = PostSerializer(data=post)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"error": serializer.errors}, status=400)

        return Response({
            "status": "success",
            "message": "Синхронизация завершена"
        }, status=200)

class PostsListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostCursorPagination

class CommentAddView(APIView):
    def post(self, request, post_id):
        access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')

        message = request.data.get("message")
        if not message:
            return Response({"error": "Message is required", "text": message}, status=400)

        url = f"https://graph.instagram.com/v25.0/{post_id}/comments"

        params = {
            "message": message,
            "access_token": access_token
        }

        response = requests.post(url, data=params)
        data = response.json()

        if "error" in data:
            return Response({"error": data["error"]}, status=400)

        comment_id = data["id"]

        info_comment_url = f"https://graph.facebook.com/v25.0/{comment_id}"
        params = {
            "fields": "id,text,username,timestamp",
            "access_token": access_token
        }
        info_comment_response = requests.get(info_comment_url, params=params)
        info_comment_data = info_comment_response.json()

        if "error" in info_comment_data:
            return Response({"error": info_comment_data["error"]}, status=400)

        serializer = CommentSerializer(data=info_comment_data)
        if serializer.is_valid():
            serializer.save()

        return Response({
            "status": "success",
            "message": "Комментарий успешно добавлен",
            "comment": info_comment_data
        }, status=200)
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
    def post(self, request):
        pass
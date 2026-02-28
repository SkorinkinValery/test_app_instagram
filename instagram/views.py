from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import generics
from typing import List
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet

from instagram.models import Post
from instagram.pagination import PostCursorPagination
from instagram.serializers import PostSerializer, CommentSerializer
from instagram.services import get_all_posts, add_comment


class SyncView(APIView):
    def post(self, request: Request) -> Response:
        try:
            all_posts = get_all_posts()
        except Exception as e:
            return Response({"error": "Failed get posts from Instagram", "info": str(e)},
                            status=400)

        posts_ids: List[str] = []
        for post in all_posts:
            serializer = PostSerializer(data=post)
            if serializer.is_valid():
                serializer.save()
                posts_ids.append(post["id"])
            else:
                return Response({"error": "Invalid data from Instagram","info": serializer.errors},
                                status=400)

        Post.objects.exclude(id__in=posts_ids).delete()

        return Response({
            "status": "success",
            "message": "Synchronization completed"
        }, status=200)

class PostsListView(generics.ListAPIView):
    queryset: QuerySet[Post] = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostCursorPagination

class CommentAddView(APIView):
    def post(self, request: Request, post_id: str) -> Response:
        post: Post = get_object_or_404(Post, id=post_id)

        message: str | None = request.data.get("message")
        if not message:
            return Response({"error": "Message is required"}, status=400)

        try:
            data = add_comment(post_id, message)
        except Exception as e:
            return Response({"error": "Failed add comment to post", "info": str(e)},
                            status=400)

        comment_id: str = data["id"]
        if not comment_id:
            return Response({"error": 'No comment id'}, status=400)

        serializer = CommentSerializer(data={
            "id": comment_id,
            "post": post.id,
            "username": "me",
            "message": message
        })
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"error": "Invalid comment data", "info": serializer.errors},
                            status=400)

        return Response({
            "status": "success",
            "message": "Comment added",
            "comment": serializer.data
        }, status=200)
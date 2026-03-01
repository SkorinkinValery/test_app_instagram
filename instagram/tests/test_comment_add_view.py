import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone

from instagram.models import Post, Comment


@pytest.mark.django_db
class TestCommentAddView:

    def setup_method(self):
        self.client = APIClient()

    @patch("instagram.views.add_comment")
    def test_create_comment_success(self, mock_add_comment):
        post = Post.objects.create(
            id="123",
            media_type="IMAGE",
            timestamp=timezone.now(),
        )

        mock_add_comment.return_value = {"id": "999"}

        url = reverse("instagram:comment", args=[post.id])

        response = self.client.post(
            url,
            {"message": "Test comment"},
            format="json"
        )

        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["comment"]["id"] == "999"
        assert response.data["comment"]["message"] == "Test comment"

        comment = Comment.objects.get(id="999")
        assert comment.post == post
        assert comment.message == "Test comment"
        assert comment.username == "me"

    def test_post_not_exists_in_db(self):
        url = reverse("instagram:comment", args=["not_exists"])

        response = self.client.post(
            url,
            {"message": "Test comment"},
            format="json"
        )

        assert response.status_code == 404
        assert Comment.objects.count() == 0

    @patch("instagram.views.add_comment")
    def test_post_exists_but_not_in_instagram(self, mock_add_comment):
        post = Post.objects.create(
            id="123",
            media_type="IMAGE",
            timestamp=timezone.now(),
        )

        mock_add_comment.side_effect = Exception("Instagram API error")

        url = reverse("instagram:comment", args=[post.id])

        response = self.client.post(
            url,
            {"message": "Test comment"},
            format="json"
        )

        assert response.status_code == 400
        assert response.data["error"] == "Failed add comment to post"
        assert Comment.objects.count() == 0


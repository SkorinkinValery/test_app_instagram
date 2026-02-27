from django.db import models


class Post(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    media_type = models.CharField(max_length=50, blank=True)
    media_url = models.URLField(max_length=1000, blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    permalink = models.URLField(blank=True, null=True)
    like_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shortcode = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post {self.id}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    ig_comment_id = models.CharField(max_length=50, blank=True, null=True)
    text = models.TextField()
    username = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.post.id}: {self.text}"
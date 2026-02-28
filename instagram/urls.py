from django.urls import path
from instagram.views import *

app_name = 'instagram'

urlpatterns = [
    path('sync/', SyncView.as_view(), name='sync'),
    path('posts/', PostsListView.as_view(), name='posts'),
    path('posts/<str:post_id>/comment/', CommentAddView.as_view(), name='comment'),
]

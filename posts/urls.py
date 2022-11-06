from django.urls import path, include
from .views import CommentDeleteView, PostCreateView, PostDetailView, PostListView, PostUpdateView, PostDeleteView, PostLikeView, CommentView, CommentDeleteView, UsersPostListView

app_name='posts'

urlpatterns = [
    path('',PostListView.as_view(),name='home'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('like/<int:pk>/',PostLikeView,name='post-like'),
    path('comment/<int:pk>/add/',CommentView.as_view(),name='comment'),
    path('comment/<int:pk>/delete/',CommentDeleteView.as_view(),name='comment-delete'),
    path('user/<str:username>', UsersPostListView.as_view(), name='user-post'),
]

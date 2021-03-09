"""
    Created by minul on 3/3/21
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/signup/', views.signup, name='signup'),
    path('new-post/', views.new_post, name='new-post'),
    path('my-post/', views.my_post, name='my-post'),
    path('post-detail/<str:slug>/', views.post_detail, name='post-detail'),
    path('publish-post/<str:slug>/', views.publish_post, name="publish-post"),
    path('delete-post/<str:slug>/', views.PostDeleteView.as_view(), name='delete-post'),
    path('post-edit/<str:slug>/', views.post_edit, name="post-edit"),
    path('user/<str:username>/', views.user_profile, name="user-profile"),
    path('add-comment/<str:slug>/', views.add_comment, name="add-comment"),
    path('approve-comment/<str:pk>/', views.approve_comment, name="approve-comment"),
    path('remove-comment/<str:pk>/', views.remove_comment, name='remove-comment'),
    path('approved-comments/<str:slug>/', views.approved_comments, name="approved-comments"),
]

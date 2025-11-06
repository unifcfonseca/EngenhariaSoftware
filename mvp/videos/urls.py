from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('minhas-aulas/', views.my_videos, name='my_videos'),  # 👈 nova rota
    path('upload/', views.upload_video, name='upload_video'),
    path('<int:video_id>/', views.video_detail, name='video_detail'),
    path('<int:video_id>/like/', views.like_video, name='like_video'),
    path('<int:video_id>/dislike/', views.dislike_video, name='dislike_video'),
]

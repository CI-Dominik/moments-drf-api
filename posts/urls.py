from django.urls import path
from posts import views_BACKUP

urlpatterns = [
    # Route für die APIView
    path('posts/', views_BACKUP.PostList.as_view()),
    path('posts/<int:pk>', views_BACKUP.PostDetail.as_view())
]

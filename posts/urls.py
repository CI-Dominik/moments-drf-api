from django.urls import path
from posts import views

urlpatterns = [
    # Route für die APIView
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>', views.PostDetail.as_view())
]

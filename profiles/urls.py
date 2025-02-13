from django.urls import path
from profiles import views_BACKUP

urlpatterns = [
    path('profiles/', views_BACKUP.ProfileList.as_view()),
    path('profiles/<int:pk>/', views_BACKUP.ProfileDetail.as_view())
]

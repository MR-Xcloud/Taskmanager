from django.urls import path
from .views import RateLimitedView, TaskListCreateView, TaskDetailView, register_user, CustomTokenObtainPairView, CustomTokenRefreshView, UserListView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('register/', register_user, name='register-user'),
    path('jwt/login/', CustomTokenObtainPairView.as_view(), name='jwt-login'),
    path('jwt/refresh/', CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('rate-limited/', RateLimitedView.as_view(), name='rate-limited'),
]

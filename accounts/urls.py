from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from accounts.api import views 

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<str:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]
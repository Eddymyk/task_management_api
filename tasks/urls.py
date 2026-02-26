from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import HttpResponse

from .views import TaskViewSet, CategoryViewSet, RegisterView, LoginView

# Home page
def home(request):
    return HttpResponse("Welcome to Task Management API!")

# Router
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')

# URL Patterns
urlpatterns = [
    # Home
    path('', home, name='home'),

    # Authentication
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API routes
    path('api/', include(router.urls)),
]
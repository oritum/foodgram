from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import UserManagementViewSet

app_name = 'users'

router = SimpleRouter()
router.register('', UserManagementViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]

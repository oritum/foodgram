from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import IngredientViewSet, RecipeManagementViewSet, TagViewSet

app_name = 'api'

router = SimpleRouter()
router.register('recipes', RecipeManagementViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include('users.urls')),
]

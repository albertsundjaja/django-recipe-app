from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views


# this will create automatic routes
# for all our viewsets
router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    # we match all routes given to this recipe app
    # to the auto generated urls by the DefaultRouter
    path('', include(router.urls))
]

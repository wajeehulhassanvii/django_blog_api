from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog import views

# router registers appropriate urls for all the actions in viewset
# /api/recipe/tag/<id>

router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'blog'

urlpatterns = [
    path('', include(router.urls))
]

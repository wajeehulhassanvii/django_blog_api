from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt import views as jwt_views

from blog import views

# router registers appropriate urls for all the actions in viewset
# /api/recipe/tag/<id>

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('my_posts', views.MyPostViewSet, 'my_post')
router.register('post', views.PostViewSet, 'post')

app_name = 'blog'

urlpatterns = [
    path('', include(router.urls))
]

from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    # in url, the first argument is the url,
    # the second is the class it maps to, in the "views" file
    # the third is the name used by the reverse function,
    # or for the function in "serializer" (not sure)
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me')
]

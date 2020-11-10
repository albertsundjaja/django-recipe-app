from django.urls import path

from . import views

# this will be used in reverse(user:xxx)
app_name = 'user'

# the name will be used in reverse e.g. reverse(user:create)
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]

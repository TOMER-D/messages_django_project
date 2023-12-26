from django.urls import path
from .views import register, get_token_view, json_login, json_logout
# from .views import get_user_id


urlpatterns = [
    path('register', register, name='register'),
    path('token', get_token_view, name='token'),
    path('login', json_login, name='login'),
    path('logout', json_logout, name='logout'),
    # for debug
    # path('get_id', get_user_id, name='get_user_id'),
]
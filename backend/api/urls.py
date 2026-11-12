from django.urls import path
from api.views import auth_view, user_view, chat_view

urlpatterns = [
    # CSRF
    path('csrf/', auth_view.csrf_token, name="csrf"),

    # Anonymous user endpoints
    path('register/', auth_view.register, name="register"),
    path('login/', auth_view.user_login, name="login"),

    # Authenticated user endpoints
    path('dashboard/', user_view.dashboard, name="dashboard"),
    path('profile/', user_view.profile, name="profile"),
    path('chat/', chat_view.chat, name="chat"),
    path('active_user/', user_view.active_user, name="active_user"),
    path('logout/', auth_view.user_logout, name="logout"),

]
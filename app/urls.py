from django.urls import path

from app import views

urlpatterns = [
    path('', views.newest, name="newest"),
    path('hot', views.hot, name="hot"),
    path('settings/profile', views.user_settings, name="user_settings"),
    path('question/<int:question_id>', views.question, name='question'),
    path('login', views.login, name='login'),
    path('registration', views.registration, name='registration'),
    path('ask', views.ask, name='ask'),
    path('tag/<str:tag>', views.get_by_tag, name='search_by_tag'),
    path('logout', views.logout, name='logout'),
]

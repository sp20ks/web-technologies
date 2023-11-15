from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('profile/', views.profile, name='profile'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('question/', views.question, name='question_default'),
    path('tag/<str:tag>/', views.tag, name='tag'),

]

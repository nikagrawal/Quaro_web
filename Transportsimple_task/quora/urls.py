from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ="home"),
    path('login/', views.login_user, name ='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_question',views.create_question, name="add_question"),
    path('question/<int:pk>/', views.question_detail, name="question_detail"),
    path('answer/like/<int:pk>/', views.like_answer, name='like_answer'),

]
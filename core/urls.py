from django.urls import path
from . import views
urlpatterns = [
    path('',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('verify/<auth_token>/',views.email_verify,name='verify'),
]

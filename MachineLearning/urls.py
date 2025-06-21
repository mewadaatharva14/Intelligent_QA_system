from django.urls import path
from . import views
urlpatterns = [
    path('',views.transformer,name='transformer'),
    path('index/',views.index,name='home'),
    path('login/',views.login_view,name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/',views.login_view,name='logout')
]
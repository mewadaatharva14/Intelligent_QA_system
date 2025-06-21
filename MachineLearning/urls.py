from django.urls import path
from . import views
urlpatterns = [
    path('transformer/',views.transformer,name='transformer'),
    path('home/',views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/',views.login_view,name='logout')
]
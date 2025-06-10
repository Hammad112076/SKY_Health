from django.contrib import admin
from django.urls import path
from app_name import views  # replace 'app_name' with your actual app folder name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('blist/', views.blist, name='blist'),
]
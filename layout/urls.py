from django.urls import path

from layout import views

app_name = 'layout'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]

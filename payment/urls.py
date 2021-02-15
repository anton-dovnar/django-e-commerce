from django.urls import path

from payment import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.ProcessView.as_view(), name='process'),
    path('done/', views.DoneTemplateView.as_view(), name='done'),
    path('canceled/', views.CanceledTemplateView.as_view(), name='canceled'),
]

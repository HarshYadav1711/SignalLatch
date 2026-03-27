from django.urls import path

from .views import ServicesHealthView

app_name = 'services'

urlpatterns = [
    path('health/', ServicesHealthView.as_view(), name='health'),
]

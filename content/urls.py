from django.urls import path

from .views import ContentHealthView

app_name = 'content'

urlpatterns = [
    path('health/', ContentHealthView.as_view(), name='health'),
]

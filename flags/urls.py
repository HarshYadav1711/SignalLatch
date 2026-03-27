from django.urls import path

from .views import FlagsHealthView

app_name = 'flags'

urlpatterns = [
    path('health/', FlagsHealthView.as_view(), name='health'),
]

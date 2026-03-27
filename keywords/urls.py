from django.urls import path

from .views import KeywordsHealthView

app_name = 'keywords'

urlpatterns = [
    path('health/', KeywordsHealthView.as_view(), name='health'),
]

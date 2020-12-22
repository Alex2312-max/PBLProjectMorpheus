from django.urls import path
from . import views

url_patterns = [
    path("<int:id>", views.processing_view, name='processing')
]
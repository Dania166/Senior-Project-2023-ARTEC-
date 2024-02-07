from django.urls import path

from text_classifier import views

app_name = 'text_classifier'

urlpatterns = [
    path('', views.classify_text, name='classify_text'),
]

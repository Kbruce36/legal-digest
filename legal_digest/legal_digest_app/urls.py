from django.urls import path
from . import views

app_name = 'legal_digest_app'

urlpatterns = [
    path('', views.index, name='index'),
]
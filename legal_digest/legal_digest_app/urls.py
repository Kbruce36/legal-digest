from django.urls import path
from . import views

app_name = 'legal_digest_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cases/new/', views.case_create, name='case_create'),
    path('cases/<slug:slug>/', views.case_detail, name='case_detail'),
    path('cases/<slug:slug>/edit/', views.case_edit, name='case_edit'),
    path('cases/<slug:slug>/delete/', views.case_delete, name='case_delete'),
    path('logout/', views.logout_view, name='logout'),
]
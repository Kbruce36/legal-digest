from django.urls import path
from . import views

app_name = 'legal_digest_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('cases/', views.public_cases_list, name='public_cases_list'),
    path('cases/<slug:slug>/', views.public_case_detail, name='public_case_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/cases/new/', views.case_create, name='case_create'),
    path('dashboard/cases/<slug:slug>/', views.case_detail, name='case_detail'),
    path('dashboard/cases/<slug:slug>/edit/', views.case_edit, name='case_edit'),
    path('dashboard/cases/<slug:slug>/delete/', views.case_delete, name='case_delete'),
    path('logout/', views.logout_view, name='logout'),
]
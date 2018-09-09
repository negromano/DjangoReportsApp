from django.urls import path, include, re_path

from core import views

app_name = "core"

urlpatterns = [
    path('', views.index, name="index"),
    path('acerca', views.acerca, name="acerca"),
    path('oracle', views.oracle, name='oracle'),
    re_path(r'^pdf/', views.download_pdf_report, name="pdf_report"),
    re_path(r'^excel/', views.download_excel_report, name="excel_report"),
]

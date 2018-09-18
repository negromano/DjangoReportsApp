from django.urls import path, include, re_path

from core import views

app_name = "core"

urlpatterns = [
    path('', views.index, name="index"),
    path('acerca', views.acerca, name="acerca"),
    path('oracle', views.oracle, name='oracle'),
    path('tabla-sencilla/tipo1', views.tabla_sencilla_tipo_1, name='tipo1_1'),
    path('tabla-sencilla/tipo2', views.tabla_sencilla_tipo_2, name='tipo1_2'),
    path('tabla-sencilla/tipo3', views.tabla_sencilla_tipo_3, name='tipo1_3'),
    path('tabla-funcion/tipo1', views.tabla_funcion_tipo_1, name='tipo2_1'),
    path('tabla-funcion/tipo2', views.tabla_funcion_tipo_2, name='tipo2_2'),
    path('tabla-funcion/tipo3', views.tabla_funcion_tipo_3, name='tipo2_3'),
    path('dos-tablas-sencillas/tipo1', views.dos_tablas_sencillas_tipo_1, name='tipo3_1'),
    path('dos-tablas-sencillas/tipo2', views.dos_tablas_sencillas_tipo_2, name='tipo3_2'),
    path('dos-tablas-sencillas/tipo3', views.dos_tablas_sencillas_tipo_3, name='tipo3_3'),
    path('dos-tablas-funcion/tipo1', views.dos_tablas_funcion_tipo_1, name='tipo4_1'),
    path('dos-tablas-funcion/tipo2', views.dos_tablas_funcion_tipo_2, name='tipo4_2'),
    path('customer', views.customer_function, name='customer'),
    re_path(r'^pdf/', views.download_pdf_report, name="pdf_report"),
]

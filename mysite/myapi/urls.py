
from django.urls import path
from . import views

urlpatterns = [
    path('', views.scan_and_insert_view, name='default_scan'), 
    path('scan/', views.scan_and_insert_view, name='scan_and_insert'),
    # path('', views.barcode_scan, name='barcode_scan'),
]
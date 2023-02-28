
from django.urls import path
from .views import scan_and_insert,barcode_scan


urlpatterns = [
    path('scan-and-insert/', scan_and_insert, name='scan_and_insert'),
    path('barcode_scan/', barcode_scan, name='barcode_scan'),
]
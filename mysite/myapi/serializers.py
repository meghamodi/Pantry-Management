from rest_framework import serializers
from .models import Inventory

class InventorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inventory
        fields = ('item_id','item_barcode','item_name')
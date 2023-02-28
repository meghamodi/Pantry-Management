from tkinter.tix import AUTO
from django.db import models

class Inventory(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_barcode = models.CharField(max_length=120)
    item_name = models.CharField(max_length=120)

    def __str__(self):
        return self.item_name

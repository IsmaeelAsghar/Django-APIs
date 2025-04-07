from django.contrib import admin

# Register your models here.
from .models import Item

# Register the Item model with the Django admin interface
admin.site.register(Item)
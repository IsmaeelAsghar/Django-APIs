from django.urls import path
from .views import item_view  # Correct import from views.py

urlpatterns = [
    path('items/', item_view),  # Route to the 'item_view' function
    
]




# from django.shortcuts import render


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.db import models
# import json

# # View function to handle GET and POST requests
# @csrf_exempt
# def item_view(request):
#     if request.method == 'GET':
#         items = item.objects.all()  # Fetch all items from the database
#         data = [{"id": item.id, "name": item.name} for item in items]
#         return JsonResponse(data, safe=False)

#     elif request.method == 'POST':
#         body = json.loads(request.body)  # Parse JSON request body
#         item = item.objects.create(name=body['name'])  # Create the item in DB
#         return JsonResponse({"id": item.id, "name": item.name})




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item  # Import the Item model
import json

# View function to handle GET, POST, PUT, DELETE requests
@csrf_exempt  # Disable CSRF protection (use with caution)
def item_view(request, item_id=None):
    # GET request to fetch all items
    if request.method == 'GET':
        if item_id:
            try:
                item = Item.objects.get(id=item_id)  # Fetch item by ID
                return JsonResponse({"id": item.id, "name": item.name})
            except Item.DoesNotExist:
                return JsonResponse({"error": "Item not found"}, status=404)
        
        items = Item.objects.all()  # Fetch all items
        data = [{"id": item.id, "name": item.name} for item in items]
        return JsonResponse(data, safe=False)

    # POST request to create a new item
    elif request.method == 'POST':
        body = json.loads(request.body)  # Parse JSON request body
        item = Item.objects.create(name=body['name'])  # Create the item in DB
        return JsonResponse({"id": item.id, "name": item.name}, status=201)

    # PUT request to update an existing item
    elif request.method == 'PUT':
        if item_id:
            try:
                item = Item.objects.get(id=item_id)  # Fetch the item by ID
                body = json.loads(request.body)  # Parse JSON request body
                item.name = body['name']  # Update item name
                item.save()  # Save updated item to the DB
                return JsonResponse({"id": item.id, "name": item.name})
            except Item.DoesNotExist:
                return JsonResponse({"error": "Item not found"}, status=404)
        
        return JsonResponse({"error": "Item ID is required for update"}, status=400)

    # DELETE request to delete an item
    elif request.method == 'DELETE':
        if item_id:
            try:
                item = Item.objects.get(id=item_id)  # Fetch the item by ID
                item.delete()  # Delete the item from the DB
                return JsonResponse({"message": "Item deleted successfully"})
            except Item.DoesNotExist:
                return JsonResponse({"error": "Item not found"}, status=404)
        
        return JsonResponse({"error": "Item ID is required for deletion"}, status=400)

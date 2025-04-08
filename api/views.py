from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Category
import json

@csrf_exempt
def item_view(request, item_id=None):
    if request.method == 'GET':
        if item_id:
            try:
                item = Item.objects.get(id=item_id)
                return JsonResponse({
                    "id": item.id,
                    "name": item.name,
                    "price": float(item.price),
                    "category": item.category.name if item.category else None,
                    "created_at": item.created_at
                })
            except Item.DoesNotExist:
                return JsonResponse({"error": "Item not found"}, status=404)

        items = Item.objects.all()
        data = [{
            "id": item.id,
            "name": item.name,
            "price": float(item.price),
            "category": item.category.name if item.category else None,
            "created_at": item.created_at
        } for item in items]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            category = Category.objects.get(id=body['category_id']) if 'category_id' in body else None
            item = Item.objects.create(
                name=body['name'],
                price=body['price'],
                category=category
            )
            return JsonResponse({
                "id": item.id,
                "name": item.name,
                "price": float(item.price),
                "category": item.category.name if item.category else None
            }, status=201)
        except Category.DoesNotExist:
            return JsonResponse({"error": "Invalid category ID"}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {e}"}, status=400)

    elif request.method == 'PUT':
        if not item_id:
            return JsonResponse({"error": "Item ID is required for update"}, status=400)

        try:
            item = Item.objects.get(id=item_id)
            body = json.loads(request.body)
            item.name = body.get('name', item.name)
            item.price = body.get('price', item.price)

            if 'category_id' in body:
                try:
                    item.category = Category.objects.get(id=body['category_id'])
                except Category.DoesNotExist:
                    return JsonResponse({"error": "Invalid category ID"}, status=400)

            item.save()
            return JsonResponse({
                "id": item.id,
                "name": item.name,
                "price": float(item.price),
                "category": item.category.name if item.category else None
            })
        except Item.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

    elif request.method == 'DELETE':
        if not item_id:
            return JsonResponse({"error": "Item ID is required for deletion"}, status=400)

        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            return JsonResponse({"message": "Item deleted successfully"})
        except Item.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

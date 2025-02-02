import json

from django.http import HttpResponse
from .models import TodoItem, CustomUser
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def check_user(request):
    username = request.GET.get('username')
    user = None
    status_code = 400

    if username:
        status_code = 204
        user, created = CustomUser.objects.update_or_create(username=username)
        if created:
            status_code = 201

    return HttpResponse(status=status_code)


@csrf_exempt
def todo_items(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON payload
            name = data.get('name')
            is_checked = data.get('is_checked', False)
            username = data.get('username')

            if not name or not username:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            user = CustomUser.objects.get(username=username)
            todo_item = TodoItem.objects.create(
                name=name,
                is_checked=is_checked,
                user=user
            )

            return JsonResponse({'message': 'Todo item created', 'todo_id': todo_item.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            id = data.get('id')
            username = data.get('username')

            if not username:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            user = CustomUser.objects.get(username=username)
            todo_item = TodoItem.objects.get(
                id=id,
                user=user
            ).delete()

            return JsonResponse({'message': 'Todo item deleted'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            id = data.get('id')
            name = data.get('name', '')
            is_checked = data.get('is_checked', False)
            username = data.get('username')

            if not username:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            try:
                todo_item = TodoItem.objects.get(id=id)
            except TodoItem.DoesNotExist:
                return JsonResponse({'error': 'Invalid to do item id'}, status=400)

            todo_item.is_checked = is_checked
            if name:
                todo_item.name = name
            todo_item.save()

            return JsonResponse({'message': 'Todo item update', 'todo_id': todo_item.id}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if request.method == 'GET':
        try:
            username = request.GET.get('username')

            user = CustomUser.objects.get(username=username)
            todo_items = TodoItem.objects.filter(user=user)
            todo_items_data = [
                {
                    'id': item.id,
                    'name': item.name,
                    'is_checked': item.is_checked,
                    'user': item.user.id
                }
                for item in todo_items
            ]

            return JsonResponse(todo_items_data, safe=False, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            if not username or not email or not password:
                return JsonResponse({'error': 'All fields are required'}, statues=400)

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email must be unique'}, status=400)


            # Create the user
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
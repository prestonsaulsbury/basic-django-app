import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from userstest.models import CustomUser


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


from django.http import JsonResponse
from .models import TodoItem, CustomUser


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

import datetime
import json
import jwt

from django.http import HttpResponse
from .models import TodoItem, CustomUser
from .email_service import EmailService
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re

def get_user_from_token(request):
    token = request.COOKIES.get('todo_token')
    if not token:
        return None
    try:
        payload = jwt.decode(token, 'SOME_STRING', algorithms=['HS256'])
        user = CustomUser.objects.get(id=payload['id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.DecodeError, CustomUser.DoesNotExist):
        return None


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

            if not name:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            user = get_user_from_token(request)
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

            user = get_user_from_token(request)
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

            try:
                user = get_user_from_token(request)
                todo_item = TodoItem.objects.get(id=id, user=user)
            except TodoItem.DoesNotExist:
                return JsonResponse({'error': 'Invalid to do item id or invalid user'}, status=400)

            todo_item.is_checked = is_checked
            if name:
                todo_item.name = name
            todo_item.save()

            return JsonResponse({'message': 'Todo item update', 'todo_id': todo_item.id}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if request.method == 'GET':
        try:

            user = get_user_from_token(request)
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
                return JsonResponse({'error': 'All fields are required'}, status=400)

            username_pattern = r"^[a-zA-Z]{3,64}$"
            match = re.search(username_pattern, username)

            print(match)

            if not match:
                print("Pattern not found.")
                return JsonResponse({'error': 'No Special Characters or Digits Allowed in User Name'}, status=400)

            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            match = re.search(email_pattern, email)
            if not match:
                print("Pattern not found.")
                return JsonResponse({'error': 'Please Enter a Valid Email Address'}, status=400)

            password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,64}$"

            match = re.search(password_pattern, password)
            if not match:
                print("Pattern not found.")
                return JsonResponse({'error': 'Password must be between 8-64 characters, include at least one uppercase, one lowercase letter, one number, and one special character'}, status=400)

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

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            user = CustomUser.objects.get(email=email)
            valid_password = user.check_password(password)
            if valid_password:
                # Generate JWT
                payload = {
                    'id': user.id,
                    'email': user.email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=14),  # Expire in 1 day
                    'iat': datetime.datetime.utcnow()
                }
                token = jwt.encode(payload, 'SOME_STRING', algorithm='HS256')

                response = JsonResponse({'message': 'User login successfully'})
                response.set_cookie(
                    key='todo_token',
                    value=token,
                    httponly=True,  # 🔥 Ensures security but still sends cookie
                    secure=False,  # ✅ Must be False for HTTP localhost
                    samesite="Lax",  # ✅ Required for localhost authentication
                    path="/"  # ✅ Makes cookie accessible across all routes
                )

                return response

            return JsonResponse({'error': 'Invalid email or password'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def user_me(request):
    if request.method == 'GET':
        user = get_user_from_token(request)
        if user:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_joined': user.date_joined,
            }
            return JsonResponse(user_data, status=200)
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            user = CustomUser.objects.get(email=email)
            token = user.generate_reset_token()

            name = user.first_name if user.first_name else 'User'
            EmailService.send_email(user.email, name, 'reset_password', {'reset_link': f'http://localhost:3000/reset-password/{token}'})
            return JsonResponse({}, status=200)


        except CustomUser.DoesNotExist:
            return JsonResponse({}, status=400)
    return JsonResponse({}, status=400)




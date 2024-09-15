from django.http import HttpResponse, JsonResponse

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


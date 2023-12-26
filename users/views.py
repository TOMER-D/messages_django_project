import logging
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
import utils


logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET"])
def get_token_view(request):
    return JsonResponse({'csrfToken': get_token(request)}, status=200)


@require_http_methods(["POST"])
def register(request: HttpRequest):
    data = utils.funcs.read_request(request=request)
    username = data["username"]
    email = data["email"]
    password = data["password"]
    missing_fields = utils.funcs.check_missing_fields(username=username, email=email, password=password)
    if missing_fields:
        return JsonResponse(data={"error": f"The fields : {missing_fields}, are missing"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse(data={"error": "Username already exists. Please choose a different username."}, status=400)
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    logger.info(f"A new user has been created, with the username: '{user.username}'")
    return JsonResponse(data={"status": "success"}, status=200)


@login_required
@require_http_methods(["POST"])
def json_logout(request):
    try:
        logout(request)
        return JsonResponse(data={"status": "success"}, status=200)
    except Exception as e:
        logger.warning(f"error: '{e}', for user: {request.user.username}({request.user.id})")
        return JsonResponse(data={"error": "unexpected error for logout action"}, status=500)


@require_http_methods(["POST", "GET"])
def json_login(request):
    data = utils.funcs.read_request(request=request)
    username = data.get('username')
    password = data.get('password')
    missing_fields = utils.funcs.check_missing_fields(username=username, password=password)
    if missing_fields:
        return JsonResponse(data={"error": f"The fields : {missing_fields}, are missing"}, status=400)
    try:
        user = authenticate(username=username, password=password)
    except Exception as e:
        logger.warning(f"error: '{e}', for username: '{username}'")
        return JsonResponse(data={'error': 'internal error'}, status=500)
    if user is not None:
        try:
            login(request, user)
            return JsonResponse(data={'status': 'success'}, status=200)
        except Exception as e:
            logger.warning(f"error: '{e}', for user: '{user}'(username: {username})")
            return JsonResponse(data={'error': 'internal error'}, status=500)
    return JsonResponse({'error': 'authentication failed'}, status=401)


# @login_required
# @require_http_methods(["GET"])
# def get_user_id(request: HttpRequest):
#     return JsonResponse(data={"user_id": request.user.id})

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
import json
from . import models
import utils
import logging


logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["POST"])
def write_message(request: HttpRequest):
    data = {}
    if request.body:
        data = json.loads(request.body)  # type: dict
    receiver_id, body, subject = data.get('receiver_id'), data.get('body'), data.get('subject')
    missing_fields = utils.funcs.check_missing_fields(
        receiver_id=receiver_id,
        body=body,
        subject=subject,
    )
    receiver_id = int(receiver_id)
    if missing_fields:
        return JsonResponse(status=400, data={"error": f"The fields : {missing_fields}, are missing"})
    try:
        receiver = models.User.objects.get(id=receiver_id)
    except models.User.DoesNotExist:
        return JsonResponse(status=404, data={f"error": f"The receiver_id: '{receiver_id}' is not exists"})
    message = models.Message(sender=request.user, receiver=receiver, body=body, subject=subject)
    message.save()
    logger.info('A new message has been created')
    return JsonResponse(status=200, data={"message_id": message.id})


@login_required
@require_http_methods(["GET"])
def read_message(request: HttpRequest):
    data = utils.funcs.read_request(request=request)
    message_id = data.get('message_id')
    missing_fields = utils.funcs.check_missing_fields(
        message_id=message_id,
    )
    if missing_fields:
        return JsonResponse(status=400, data={"error": f"The fields : {missing_fields}, are missing"})
    try:
        message = models.Message.objects.get(id=message_id, sender=request.user)
    except models.Message.DoesNotExist:
        return JsonResponse(status=404, data={"error": f"message id: '{message_id}' is not found"})
    data = message.read()
    logger.info(f"The message by id '{message.id}' was read")
    return JsonResponse(status=200, data=data)


@login_required
@require_http_methods(["GET"])
def get_messages_per_receiver(request: HttpRequest):
    messages_query_set = models.Message.objects.filter(receiver=request.user).all()
    messages = {"messages_id": [message.id for message in messages_query_set]}
    return JsonResponse(status=200, data=messages)


@login_required
@require_http_methods(["GET"])
def get_unread_per_receiver(request: HttpRequest):
    messages_query_set = models.Message.objects.filter(receiver=request.user, is_read=False).all()
    messages = {"messages_id": [message.id for message in messages_query_set]}
    return JsonResponse(status=200, data=messages)


def user_is_not_sender_and_not_receiver(message: models.Message, request: HttpRequest) -> bool:
    user_id = request.user.id
    if not user_id == message.sender.id and not user_id == message.receiver.id:
        return True
    return False


@login_required
@require_http_methods(["DELETE"])
def delete_message(request: HttpRequest):
    data = utils.funcs.read_request(request=request)
    message_id = data.get('message_id')
    try:
        message = models.Message.objects.get(id=message_id)
    except not models.Message.DoesNotExist:
        return JsonResponse(status=404, data={"error": f"Message ID '{message_id}' is not exists"})
    if user_is_not_sender_and_not_receiver(message=message, request=request):
        logger.warning(f"The user '{request.user.id}' tried to delete a message '{message_id}' that was not his own")
        return JsonResponse(status=403, data={"error": "You are not allowed to delete this message"})
    message.delete()
    logger.info(f"The message '{message_id}' has been deleted")
    return JsonResponse(status=200, data={"status": "success"})
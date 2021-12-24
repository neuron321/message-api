from django.core.cache import cache
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .functions import get_phonenumber_obj, is_number_valid
from .serializers import SMSSerializer


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def SMSList(request, format=None):

    data = request.data

    try:
        sender = data['sender']
    except:
        return Response({"message": "", "error": "sender is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        to = data['to']
    except:
        return Response({"message": "", "error": "to is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not is_number_valid(sender):
        return Response({"message": "", "error": "sender is invalid"}, status=status.HTTP_400_BAD_REQUEST)

    if not is_number_valid(to):
        return Response({"message": "", "error": "to is invalid"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        assert len(data['text']) > 0
    except:
        return Response({"message": "", "error": " text is missing"}, status=status.HTTP_400_BAD_REQUEST)

    to_num = get_phonenumber_obj(to)
    if to_num == -1:
        return Response({"message": "", "error": "to parameter not found"}, status=status.HTTP_404_NOT_FOUND)

    sender_num = get_phonenumber_obj(sender)
    if sender_num == -1:
        return Response({"message": "", "error": "sender parameter not found"}, status=status.HTTP_404_NOT_FOUND)

    if to_num.account.username == request.user.username:
        data['to'] = to_num.id
        data['sender'] = sender_num.id
        item = SMSSerializer(data=data)
    else:
        return Response({"message": "", "error": "to parameter not found"}, status=status.HTTP_401_UNAUTHORIZED)

    if item.is_valid():
        item.save()
        if item.data['text'] in ['STOP', 'STOP\n', 'STOP\r', 'STOP\r\n']:
            cache.set(to, sender, timeout=4*60*60)
        return Response({"message": "inbound sms ok", "error": ""}, status=status.HTTP_201_CREATED)
    else:
        return Response(item.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def OutboundSMSList(request, format=None):

    data = request.data

    try:
        sender = data['sender']
    except:
        return Response({"message": "", "error": "sender is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        to = data['to']
    except:
        return Response({"message": "", "error": "to is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not is_number_valid(sender):
        return Response({"message": "", "error": "sender is invalid"}, status=status.HTTP_400_BAD_REQUEST)

    if not is_number_valid(to):
        return Response({"message": "", "error": "to is invalid"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        assert len(data['text']) > 0
    except:
        return Response({"message": "", "error": " text is missing"}, status=status.HTTP_400_BAD_REQUEST)

    to_num = get_phonenumber_obj(to)
    if to_num == -1:
        return Response({"message": "", "error": "to parameter not found"}, status=status.HTTP_404_NOT_FOUND)

    sender_num = get_phonenumber_obj(sender)
    if sender_num == -1:
        return Response({"message": "", "error": "sender parameter not found"}, status=status.HTTP_404_NOT_FOUND)

    if sender_num.account.username == request.user.username:
        data['to'] = to_num.id
        data['sender'] = sender_num.id
        item = SMSSerializer(data=data)
    else:
        return Response({"message": "", "error": "from parameter not found"}, status=status.HTTP_401_UNAUTHORIZED)

    if cache.get(to) == sender:
        err_msg = "sms from {} to {} blocked by STOP request".format(
            sender, to)
        return Response({"message": "", "error": err_msg}, status=status.HTTP_409_CONFLICT)

    if item.is_valid():
        api_call_daily_limit = 50
        key = "limit"+str(sender)

        used_limit = cache.get(key)
        if used_limit == None:
            item.save()
            cache.set(key, 1, timeout=24*60*60)
        elif used_limit >= api_call_daily_limit:
            return Response({"message": "", "error": "limit reached for from {}".format(sender)}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        else:
            item.save()
            cache.incr(key)

        return Response({"message": "outbound sms ok", "error": ""}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": item.errors, "error": "unknow error"}, status=status.HTTP_400_BAD_REQUEST)

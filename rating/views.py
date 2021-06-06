from django.shortcuts import render
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
import json
from rating.models import User
import datetime
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken
from django.http import JsonResponse


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.
def get_login_response(data={}):
    ''' Function to get login request response'''
    get_dict = VerifyJSONWebTokenSerializer().validate(data)
    user = get_dict['user']

    try:
        user.jwt_secret = data['token']
        user.save()
        data.update({
        'user_id': get_dict['user'].id,
        'email': str(get_dict['user'].email).lower(),
        'mobile_number': get_dict['user'].mobile_number,
        'username': get_dict['user'].username,
        })
        return data

    except Exception as e:
        return JsonResponse({"status": 500,
                            "message": "Something went wrong please try after sometime.",
                            "data": data})


class ObtainJSONWebToken(ObtainJSONWebToken):

    def post(self, request, version, *args, **kwargs):
        res = super(ObtainJSONWebToken, self).post(request, args, kwargs)
        data = res.data or {}

        if data.get('token') and data['token']:
            # if organization is not provided throw error
            data = get_login_response(data)
        else:
            data.update({'status': {'code': 0, 'message': ""}})
        return JsonResponse({"status": 200,
                            "message": "Successfully Logged in",
                            "data": data})

obtain_jwt_token = ObtainJSONWebToken.as_view()

class UserCreate(APIView):

    def post(self, request, version, **kwargs):
        ''' User Sign up default and authenticate session'''
        try:
            data = request.POST.dict()
            # if mobile exists
            if len(str(data['mobile'])) != 10:
                return JsonResponse({"status": 400,
                            "message": "Please Enter 10 digit valid mobile number",
                            "data": data})
            if User.objects.filter(mobile_number=data['mobile']):
                return JsonResponse({"status": 400,
                            "message": "Email is already exist with Database",
                            "data": data})

            # if email exists
            if User.objects.filter(email__iexact=str(data['email']).lower()):
                return JsonResponse({"status": 400,
                            "message": "Email is already exist with Database",
                            "data": data})

            username = False
            while not username:
                timestamp = str(int(datetime.datetime.now().timestamp()))
                if not User.objects.filter(username=timestamp):
                    username = timestamp
            
            user = User.objects.create(email=str(data['email']).lower(),
                            mobile_number=data['mobile'], username=username)
            user.set_password(data['password'])

            user.save()

            # Authenticate user with credentials
            logged_user = authenticate(**{'username': user.username,
            'password': data['password']})
            if logged_user:
                payload = jwt_payload_handler(logged_user)
                # Get token from jwt_payload
                token = {'token': jwt_encode_handler(payload)}

                # Get user and token data using serializer
                data = get_login_response(token)
                return JsonResponse({"status": 201,
                            "message": "User Successfully SIgnup.", 
                            "data": data})
            else:
                return JsonResponse({"status": 400,
                            "message": "Bad Request",
                            "data": data})
        except Exception as e:
            return JsonResponse({"status": 500, "message": "Internal Server Error", "data": data})


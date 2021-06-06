from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


class JSONWebTokenAuthentication(JSONWebTokenAuthentication):
    def get_jwt_value(self, request):
        res = super(JSONWebTokenAuthentication, self).get_jwt_value(request)
        if res:
            token = res.decode()
            try:
                get_dict = VerifyJSONWebTokenSerializer().validate({'token': token})
                if get_dict['user'].jwt_secret == token:
                    return res
                else:
                    msg = {'status': {'code': 4, 'message': 'Invalid Signature'}}
                    raise exceptions.AuthenticationFailed(msg)
            except Exception:
                msg = {'status': {'code': 4, 'message': 'Invalid Signature'}}
                raise exceptions.AuthenticationFailed(msg)
        return res
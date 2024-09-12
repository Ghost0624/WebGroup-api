from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.http.response import JsonResponse

from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from Member.models import Members, Roles
from Member.serializers import MemberSerializer, RoleSerializer


def authentication(token):  
    auth = get_authorization_header(token).split()
    
    # Check if the authorization header is valid  
    if auth and len(auth) == 1: 
        token = auth[1].decode('utf-8')  # Decode the token  
        id = decode_access_token(token)  # Decode the access token  

        # Fetch the member based on the decoded ID  
        member = Members.objects.filter(pk=id).first()  
        if member:
            return member
        else:  
            return AuthenticationFailed('unauthenticated')
    else:  
        return AuthenticationFailed('unauthenticated')
    
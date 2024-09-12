from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.http.response import JsonResponse

import time

from .services import authentication
from .form import UploadFileForm
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from Member.models import Members, Roles
from Member.serializers import MemberSerializer, RoleSerializer

from webgroup.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import boto3


@csrf_exempt
def signUp(request):
  if request.method == "POST":
    new_member = JSONParser().parse(request)
    new_member_serializer = MemberSerializer(data=new_member)
    if new_member_serializer.is_valid():
      new_member_serializer.save()
      return JsonResponse({"ok": True}, status=200)  
    # try:  
    #   # Here you would typically save the new_member to the database  
    #   return JsonResponse({"ok": True, "member": new_member}, status=201)  
    # except Exception as e:  
    #   return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt  
def signIn(req):  
  refresh_token_cookie = req.COOKIES.get('refreshToken') 
  print(refresh_token_cookie)
  if req.method == "POST":  
    user_data = JSONParser().parse(req)  
    try:  
      user = Members.objects.filter(email=user_data['email']).first()
      if not user:
        return JsonResponse({"ok": False, "error": "The provided email address is not registered."}, status=401)
      if not user.check_password(user_data['password']):
        return JsonResponse({"ok": False, "error": "The provided password is wrong."}, status=401)

    except Members.DoesNotExist:  
      return JsonResponse({"ok": False, "error": "The provided email address is not registered."}, status=401)
        
    access_token = create_access_token(user.id)  
    refresh_token = create_refresh_token(user.id)  

    response = JsonResponse({"ok": True, "user": MemberSerializer(user).data  , "token": access_token, "refreshToken": refresh_token}, status=200)  
    response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)

    return response

@csrf_exempt
def refreshAPI(req):
  if req.method == "POST":
    
    refresh_token = req.COOKIES.get('refreshToken')
    id = decode_refresh_token(refresh_token)
    user = Members.objects.filter(id=id).first()
    user_data = MemberSerializer(user).data  
    access_token = create_access_token(id)
    refresh_token = create_refresh_token(id)
    response = JsonResponse({"ok":True, "token": access_token, "user": user_data}, status=200)
    response.set_cookie(key='refreshToken', value=refresh_token, httponly=True) 
    return response
  
@csrf_exempt
def logout(req):  
  if req.method == "POST":
    response = JsonResponse({'message': 'success'})  
    response.delete_cookie(key="refreshToken")  
    return response  
  
@csrf_exempt
def developers(req):  
  if req.method == "POST":
    # auth = get_authorization_header(req).split()
    # print(auth)
    # authentication(req)  # Ensure this function is defined elsewhere  
    developers = Members.objects.filter(role_id__isnull=False).select_related('role').order_by('?')[:3]
    serialized_developers = MemberSerializer(developers, many=True)  # Serialize the queryset  
    return  JsonResponse({"ok": True, "developers": serialized_developers.data})  # Ensure to return the response 
      
@csrf_exempt
def upload_file(req): 
  print(req.POST.get('id'))
  if req.method == 'POST':
    print(req.FILES)
    # Check if 'file' is in request.FILES  
    if 'photo' in req.FILES:
      uploaded_file = req.FILES['photo']  # Access the file safely  
      s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
      s3.upload_fileobj(uploaded_file, AWS_STORAGE_BUCKET_NAME, uploaded_file.name)

      file_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{uploaded_file.name}"
      # new_member_serializer = MemberSerializer(data={'photo': file_url})
      # if new_member_serializer.is_valid():
      #   new_member_serializer.save()
    else:  
      return JsonResponse({'error': 'No file provided'})  

    return JsonResponse({'ok': True, 'fileUrl': file_url})
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
import random
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status


# Create your views here.




@api_view(['POST'])
def register_view(request):
    email = request.data.get('email')
    if CustomUser.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    s = UserSerializers(data=request.data)
    if s.is_valid():
        user = CustomUser.objects.create_user(username = request.data.get('username'),
                                              password= request.data.get('password'),
                                              first_name = request.data.get('first_name'),
                                              last_name = request.data.get('last_name'),
                                              email = request.data.get('email'),
                                              mobile = request.data.get('mobile'),
                                              address = request.data.get('address'),
                                              location = request.data.get('location'),
                                              role = request.data.get('role'))
        token = Token.objects.create(user=user)
        print(token.key)

        # Send email with username and password
        subject = 'Welcome To Pets World'
        message = f'Dear {request.data.get("first_name")},\n\nHere are your login credentials:\n\nUsername: {request.data.get("username")}\nPassword: {request.data.get("password")}\n\nPlease keep this information secure.'
        recipient = request.data.get('email')
        
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
        except Exception as e:
            print(f"Error sending email: {e}")

        return JsonResponse({'token':token.key})
    else:
        print(s.errors)
        return Response(s.errors)
    
@api_view(['POST'])
def login_view(request):
    s = UserLoginSerializers(data=request.data)
    if s.is_valid():
        user =authenticate(username = request.data.get('username'),password = request.data.get('password'))
        if user:
            token = Token.objects.get(user=user)
            return JsonResponse({'token':token.key,
                                 'is_superuser': user.is_superuser,
                                 'role' : user.role})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
    else:
        return Response(s.errors)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_donor_list(request):

    donors = CustomUser.objects.filter(role = 'donor')
    serializers = UserSerializers(donors,many=True)
    return Response(serializers.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_donor(request, id):
    try:
        donor = CustomUser.objects.get(id=id)
        donor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Donor not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_list(request):

    users = CustomUser.objects.filter(role = 'user')
    serializers = UserSerializers(users,many=True)
    return Response(serializers.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_category(request):
    category_name = request.data.get('name')
    if Category.objects.filter(name=category_name).exists():
        return Response({'error': 'Category already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CategorySerializers(data=request.data)
    if serializer.is_valid():
        user = Category.objects.create(name=category_name,image=request.data.get('image'))
        user.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):

    categories = Category.objects.all()
    serializers = CategorySerializers(categories,many=True)
    return Response(serializers.data)  

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_category(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)  

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def donate_pet(request):
    
#     serializer = PetsDataSerializers(data=request.data)
#     if serializer.is_valid():
#         data = Category.objects.create(category=request.data.get('category'),
#                                        age=request.data.get('age'),
#                                        breed=request.data.get('breed'),
#                                        description=request.data.get('description'),
#                                        image=request.data.get('image'))
#         data.save()
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def donate_pet(request):
    serializer = PetsDataSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_donation_requests(request):

    requests = PetsData.objects.filter(status = 0)
    serializers = PetsDataSerializers(requests,many=True)
    return Response(serializers.data)  

#------------------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ok(request):

    users = UserData.objects.all()
    serializers = UserDataSerializers(users,many=True)
    arr=[]
    for user in users:
        username = {"name":user.name,"age":user.age}
        arr.append(username)
    print(arr)
    return Response(serializers.data)



class Userview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        users = UserData.objects.all()
        e = UserDataSerializers(users,many=True)
        return Response(e.data)

    def post(self,request):
        serializer = UserDataSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self,request,id=None):
        if id: 
            userobj = UserData.objects.get(id=id)
            userobj.delete()
            return JsonResponse({'data':'data deleted'})
        else:
            return JsonResponse({'error':'give an id as url param'})
        
    def put(self,request,id=None):
        if id:
            userobj = UserData.objects.get(id=id)
            s = UserDataSerializers(data=request.data)
            if s.is_valid():
                userobj.name = request.data.get('name')
                userobj.location = request.data.get('location')
                userobj.about = request.data.get('about')
                userobj.age = request.data.get('age')
                userobj.save()
                return Response(s.data)
            else:
                return Response(s.errors)

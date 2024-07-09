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
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def donate_pet(request):
    data = request.data.copy()  # Make a copy of the request data
    data['donor_id'] = request.user.id  # Add the donor's ID to the data
    print(data['donor_id'])

    serializer = PetDetailsSerializers(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_donation_requests(request):

    requests = PetDetails.objects.filter(status = 0)
    serializers = PetDetailsSerializers(requests,many=True)
    return Response(serializers.data) 

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def approve_donation_request(request, id):
    try:
        pet = PetDetails.objects.get(id=id)
    except PetDetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data
    serializer = PetDetailsSerializers(pet, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def cancel_donation_request(request, id):
    try:
        pet = PetDetails.objects.get(id=id)
    except PetDetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data
    serializer = PetDetailsSerializers(pet, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
@permission_classes([AllowAny])
def get_category_wise_data(request, id):
    try:
        pets = PetDetails.objects.filter(category_id=id,available = True,status = 1)
        serializer = PetDetailsSerializers(pets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except PetDetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adopt_pet(request):
    user = request.user
    pet_id = request.data.get('pet_id')
    print(pet_id)
    
    if not pet_id:
        return Response({'status': 'error', 'message': 'Pet ID is required'}, status=400)

    try:
        pet = PetDetails.objects.get(id=pet_id)
    except PetDetails.DoesNotExist:
        return Response({'status': 'error', 'message': 'Pet not found'}, status=404)
    
    pet.available = False
    pet.save()
    notification = AdoptionNotification.objects.create(pet=pet, user=user,message = 'Your pet has been Adopted!')
    adoption = AdoptedPets.objects.create(pet=pet, user=user)
    return Response({'status': 'success', 'message': 'Pet adopted successfully!'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_donor_notifications(request):
    notif = AdoptionNotification.objects.filter(pet__donor=request.user)
    serializers = AdoptionNotificationSerializers(notif,many=True)
    return Response(serializers.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def handle_donor_notification(request, id):
    try:
        notif = AdoptionNotification.objects.get(id=id)
    except AdoptionNotification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data
    serializer = AdoptionNotificationSerializers(notif, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notification_count(request):
    count = AdoptionNotification.objects.filter(pet__donor=request.user,status=0).count()
    rcount = PetDetails.objects.filter(status=0).count()
    return Response({'count': count,
                     'rcount':rcount})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_password(request):
    user = request.user
    data = request.data

    print(user)
    print(data)

    current_password = data.get('cp')
    new_password = data.get('np')

    # Check if the current password is correct
    if not user.check_password(current_password):
        return Response({'error': 'Current password is incorrect.'}, status=400)

    # Ensure the new password is not the same as the current password
    if current_password == new_password:
        return Response({'error': 'New password cannot be the same as the current password.'}, status=400)

    # Set the new password
    user.set_password(new_password)
    user.save()

    return Response({'success': 'Password updated successfully.'})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_purchase_details(request, id):
    try:
        print(id)
        details = AdoptedPets.objects.filter(user__id=id)
        print(details)
        serializer = AdoptedPetsSerializers(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except AdoptedPets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_donation_details(request, id):
    try:
        details = PetDetails.objects.filter(donor__id=id,status=1)
        serializer = PetDetailsSerializers(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except AdoptedPets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_pet(request,id):
    print('deletepet')
    try:
        pet = PetDetails.objects.get(id=id)
        pet.delete()
        return Response({'donor_id': pet.donor_id}, status=status.HTTP_200_OK)
    except PetDetails.DoesNotExist:
        return Response({'error': 'Pet not found'}, status=status.HTTP_404_NOT_FOUND)
   

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_data(request):

    user = request.user
    serializer = UserSerializers(user)
    print(serializer.data)
    return Response(serializer.data)
    
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_profile_data(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializers(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data

        email = request.data.get('email')
        # if 'email' in data and User.objects.filter(email=data['email']).exclude(id=user.id).exists():
        if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        username = request.data.get('username')
        if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializers(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

# @api_view(['GET', 'PUT'])
# @permission_classes([IsAuthenticated])
# def update_profile_data(request):
#     user = request.user

#     if request.method == 'GET':
#         serializer = UserSerializers(user)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         data = request.data

#         # Check if email already exists and is not the current user's email
#         if 'email' in data and User.objects.filter(email=data['email']).exclude(id=user.id).exists():
#             return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

#         # Check if username already exists and is not the current user's username
#         if 'username' in data and User.objects.filter(username=data['username']).exclude(id=user.id).exists():
#             return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = UserSerializers(user, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_adopted_pets(request):
    pets = AdoptedPets.objects.filter(user=request.user)
    serializers = AdoptedPetsSerializers(pets,many=True)
    return Response(serializers.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_donated_pets(request):
    pets = PetDetails.objects.filter(donor=request.user)
    serializers = PetDetailsSerializers(pets,many=True)
    return Response(serializers.data)
#------------------------------------------------------------------------------------


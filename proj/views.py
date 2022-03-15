from functools import partial
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view 
from .models import Client, Employee
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, EmployeeSerializer, ClientSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.contrib.auth.models import Permission
from .decorators import employee_only
from django.contrib.auth.models import Group
from .helpers import reset_email




# creating the login function and retruning the token for the user
@api_view(['POST'])
def login(request):
    # collect data from the request
    password = request.data['password']

    try:
        # get the user details
        user = User.objects.get(username = request.data['username'])
            # check the password if it's correct
        if user.check_password(password):
            token = Token.objects.create(user=user)
            return Response({'Token': token.key }, status=status.HTTP_202_ACCEPTED)  
        else: 
            return Response({'password': "not matching" }, status=status.HTTP_400_BAD_REQUEST)      
    except:
        return Response({'username': "please recheck the username" }, status=status.HTTP_400_BAD_REQUEST) 
    


# creating the logout function and deleting the token for the user
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout(request):
    request.auth.delete()
    return Response({"message": "logged out and the token is deleted"}, status=status.HTTP_202_ACCEPTED)




# reset password based of the user authonticated already 
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def change_password(request):

    user = User.objects.get(username= request.user)

    # get data from the request and validate the password
    old_password=request.data['old_password']
    new_password= request.data['new_password']
    new_password2 = request.data['new_password2']

    data = {
        "password": new_password
    }

    # validate if the old password is correct 
    if user.check_password(old_password):
        if new_password == new_password2:
    
            user.set_password(new_password)
            user.save()
            return Response({'msg':'password changed'}, status=status.HTTP_202_ACCEPTED)        
    return Response({'error':"old password is not matching"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password(request):
    email = request.data['email']

    #  check if email exisits
    if not User.objects.filter(email = email).exists():
        return Response({'msg':'please check the email again'}, status= status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.filter(email = email).values_list('id')
    print(user[0][0])
    reset_email(email, user[0][0])
    return Response({'msg':'email sent'}, status= status.HTTP_202_ACCEPTED)



# reset password based of the user authonticated already 
@api_view(['PATCH'])
def email_reset(request, id):

    user = User.objects.get(id= id)

    # get data from the request and validate the password
    password= request.data['password']
    password2 = request.data['password2']

    data = {
        "password": password
    }

    # validate if the passwords
    if password == password2:
        user.set_password(password)
        user.save()
        return Response({'msg':'password changed'}, status=status.HTTP_202_ACCEPTED)        
    return Response({'error':"old password is not matching"}, status=status.HTTP_400_BAD_REQUEST)

# ################################

# crud for the admin 

@api_view(['POST','GET'])
@permission_classes([IsAdminUser])
@authentication_classes([TokenAuthentication])
def create_list_employee(request):

    # create the employ
    if request.method == 'POST':
        data = {
            "user": request.data["user"],
            "is_active": True,
            "created_by": request.user.id,
        }
        
        # get user to add the employee group        
        user = User.objects.get(id= request.data['user'])
        my_group = Group.objects.get(name='employee') 
        my_group.user_set.add(user)

        print(user)
        print(my_group)
        # my_group.user_set.add(user)
        serializer = EmployeeSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response({'error':"it's not correct"}, status=status.HTTP_400_BAD_REQUEST)

    # get all employees
    if request.method == 'GET':
        employes = Employee.objects.all()
        serializer = EmployeeSerializer(employes, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



@api_view(['PUT','GET','DELETE'])
@permission_classes([IsAdminUser])
@authentication_classes([TokenAuthentication])
def get_edit_delete_employee(request,id):

    # edit the employ
    if request.method == 'PUT':
        employe = Employee.objects.get(user=id)
        data={
            "is_active": request.data["active"],
            "updated_by": request.user.id,
        }
        serializer = EmployeeSerializer(employe ,data= data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response({'error':"it's not correct"}, status=status.HTTP_400_BAD_REQUEST)

    # get employe
    if request.method == 'GET':
        employe = Employee.objects.get(user=id)
        serializer = EmployeeSerializer(employe)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # delete employe
    if request.method == 'DELETE':
        employe = Employee.objects.get(user=id)
        data={
            "is_active": False,
            "updated_by": request.user.id
        }
        serializer = EmployeeSerializer(employe, data = data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response({'error':"it's not correct"}, status=status.HTTP_400_BAD_REQUEST)





# ################################

# crud for the employee 

@api_view(['POST','GET'])
@authentication_classes([TokenAuthentication])
@employee_only
def create_list_client(request):

    # create the client
    if request.method == 'POST':
        data = {
            "user": request.data["user"],
            "is_active": True,
            "created_by": request.user.id,
        }
        serializer = ClientSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response({'error':"it's not correct"}, status=status.HTTP_400_BAD_REQUEST)

    # get all clients
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



@api_view(['PUT','GET','DELETE'])
@authentication_classes([TokenAuthentication])
@employee_only
def get_edit_delete_client(request,id):

    # edit the client
    if request.method == 'PUT':
        client = Client.objects.get(user=id)
        data={
            "is_active": request.data["active"],
            "updated_by": request.user.id,
        }
        serializer = ClientSerializer(client ,data= data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response({'error':"it's not correct"}, status=status.HTTP_400_BAD_REQUEST)

    # get employe
    if request.method == 'GET':
        client = Client.objects.get(user=id)
        serializer = ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # get employe
    if request.method == 'DELETE':
        client = Client.objects.get(user=id)
        data={
            "is_active": False,
            "updated_by": request.user.id
        }
        serializer = ClientSerializer(client, data = data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response({'error':"it's not correct"}, status=status.HTTP_400_BAD_REQUEST)


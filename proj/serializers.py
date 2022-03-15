from rest_framework import serializers
from .models import Client, Employee
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('__all__')


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('__all__')
        

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('__all__')



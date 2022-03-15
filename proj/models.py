from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='client_id', unique=True)
    is_active = models.BooleanField(default=True)
    updated_by=models.ForeignKey(User, related_name='updated_by_employee',on_delete=models.CASCADE, null= True, blank= True)
    created_by=models.ForeignKey(User, related_name='created_by_employee',on_delete=models.CASCADE, null= True, blank= True)    
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now = True)

    def __str__(self):
        return self.user.username
    


class Employee(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='employee_id', unique=True)
    is_active = models.BooleanField(default=True)
    updated_by=models.ForeignKey(User, related_name='updated_by_admin',on_delete=models.CASCADE,null= True, blank= True)
    created_by=models.ForeignKey(User, related_name='created_by_admin',on_delete=models.CASCADE, null= True, blank= True)    
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now = True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        pass
    
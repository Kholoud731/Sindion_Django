
from django.urls import path
from .views import login, logout, change_password, create_list_employee, get_edit_delete_employee, create_list_client, get_edit_delete_client, reset_password, email_reset



urlpatterns = [

    # auth urls
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('change-password', change_password, name="change_password"),

    # otp to reset password 
    path('reset-password', reset_password, name="reset_password"), # to send the email only 
    path('reset-password/<int:id>', email_reset, name="email_reset"), # to change the email


    # Admin CRUD
    path('employee', create_list_employee ,name="create_list_employee"),
    path('employee/<int:id>', get_edit_delete_employee ,name="get_edit_delete_employee"),

    # employee CRUD
    path('client', create_list_client ,name="create_list_client"),
    path('client/<int:id>', get_edit_delete_client ,name="get_edit_delete_client"),

    


]

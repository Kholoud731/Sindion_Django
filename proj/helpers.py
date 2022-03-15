from django.core.mail import send_mail
from django.conf import settings


def reset_email(email, id):

    send_mail(
            subject="Reset Your Password Link",
            message=f"Hello if you still wish to change your password please click on this link http://localhost:8000/reset-password/{id} ",
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[f'{email}'],
            fail_silently=False)
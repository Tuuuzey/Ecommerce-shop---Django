from django.db import models
from django.contrib.auth.models import User


class SellerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    phone_number = models.CharField(max_length=20) 
    VERIFICATION_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    verification_status = models.CharField(
        max_length=10,
        choices=VERIFICATION_CHOICES,
        default='Pending', 
    )

    def __str__(self):
        return f"{self.user.username}"
    


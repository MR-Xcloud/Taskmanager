
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)

    # def save(self, *args, **kwargs):
    #     if self.password != self.confirm_password:
    #         raise ValueError("Passwords do not match")
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks_assigned')
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Employee(models.Model):

    STATUS_CHOICES = [
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='employee'
    )

    def __str__(self):
        return self.user.username



class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('finished', 'Finished'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks')
    assigned_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks'
    )
    deadline = models.DateField(null=True, blank=True)
    submission = models.FileField(upload_to='submissions/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('status', '-created_at')

    def __str__(self):
        return self.title
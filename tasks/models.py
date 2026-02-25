from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
]

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
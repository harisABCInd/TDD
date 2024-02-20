from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    """
    Task for todo app
    """
    name = models.CharField(max_length=128)
    is_complete = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    due_date = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    notes = models.TextField(blank=True)
    completion_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', null=True, blank=True)

class Tag(models.Model):
    """
    Tags associated with each task
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
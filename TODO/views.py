from django.shortcuts import render
from rest_framework import generics
from TODO.serializers import TaskDetailSerializer, TaskSerializer
from core.models import Task

# Create your views here.

class TaskView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView);
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    
        
    
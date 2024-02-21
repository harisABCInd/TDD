from rest_framework import serializers
from core.models import Task, Tag
from user.serializers import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('id',)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task 

    fields = ['id', 'name', 'created_by', 'created_date', 'priority', 'due_date', 'notes', 'completion_date', 'assigned_to', 'tags']
    read_only_fields = ('id',)

class TaskDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    created_by = UserSerializer()
    assigned_to = UserSerializer()

    class Meta:
        model = Task 

    fields = ['id', 'name', 'created_by', 'created_date', 'priority', 'due_date', 'notes', 'completion_date', 'assigned_to', 'tags']
    read_only_fields = ('id',)

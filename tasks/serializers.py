from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Category
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def update(self, instance, validated_data):
        if instance.status == 'Completed' and validated_data.get('status') != 'Pending':
            # Prevent editing completed task unless reverted
            for key in validated_data:
                if key not in ['status', 'completed_at']:
                    raise serializers.ValidationError("Cannot edit completed task.")
        # Automatically set completed_at timestamp
        if validated_data.get('status') == 'Completed' and instance.status != 'Completed':
            instance.completed_at = timezone.now()
        elif validated_data.get('status') == 'Pending':
            instance.completed_at = None
        return super().update(instance, validated_data)
    
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['user']
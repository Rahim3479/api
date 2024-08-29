from rest_framework import serializers
from .models import Client, Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
         # Specify the model to be serialized
        model = Project
        fields = ['id', 'project_name', 'client', 'created_by', 'users']   # Define the fields


class ClientSerializer(serializers.ModelSerializer):
    # Nested serializer to include related projects
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client   # Specify the model to be serialized
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by'] #Define the fields


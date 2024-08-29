from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from rest_framework.permissions import IsAuthenticated

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    

    @action(detail=True, methods=['get'])    # Custom action to get projects for a specific client
    def projects(self, request, pk=None):    # Get the client instance
        client = self.get_object()
        projects = client.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response({
            'id': client.id,
            'client_name': client.client_name,
            'projects': serializer.data,
            'created_at': client.created_at,
            'created_by': client.created_by.username
        })
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
  

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(users=user)


    @action(detail=True, methods=['post'])
    def add_project(self, request, pk=None):
        client = Client.objects.get(pk=pk)
        data = request.data
        project_serializer = ProjectSerializer(data=data)
        if project_serializer.is_valid():
            project = project_serializer.save(client=client, created_by=request.user)
            project.users.set(data.get('users', []))    # Assign users to the project
            return Response(ProjectSerializer(project).data, status=201)
        return Response(project_serializer.errors, status=400)     # Return error response

def home(request):
    return HttpResponse("Welcome,this is api created by rahim mahagonde")   # Basic welcome response


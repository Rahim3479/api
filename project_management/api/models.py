from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    # The name of the client
    client_name = models.CharField(max_length=255)
    # Timestamp for when client created
    created_at = models.DateTimeField(auto_now_add=True)
    # Foreign key 
    # If the user is deleted, this field will be set to NULL
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.client_name

class Project(models.Model):
    # The name of the project
    project_name = models.CharField(max_length=255)
    # Foreign key linking to the Client model
    # If the client is deleted, all related projects will also be deleted
    client = models.ForeignKey(Client, related_name='projects', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.project_name


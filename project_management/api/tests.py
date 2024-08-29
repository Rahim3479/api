from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Client, Project
from rest_framework import status

class ClientTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client_data = {'client_name': 'company A'}
        self.client_instance = Client.objects.create(client_name='Nimap', created_by=self.user)

    def test_create_client(self):  #Test creation of a new client.

        response = self.client.post('/api/clients/', self.client_data, format='json')
        print("Response Data:", response.data)
        print("Response Status Code:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['client_name'], 'company A')

    def test_get_clients(self):   #Test retrieval of the list of clients.
        response = self.client.get('/api/clients/')
        print("Response Data:", response.data)
        print("Response Status Code:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_client(self):  #Test updating an existing client
        updated_data = {'client_name': 'Updated Company'}
        response = self.client.patch(f'/api/clients/{self.client_instance.id}/', updated_data, format='json')
        print("Response Data:", response.data)
        print("Response Status Code:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['client_name'], 'Updated Company')

    def test_delete_client(self):  #Test deletion of a client.
        response = self.client.delete(f'/api/clients/{self.client_instance.id}/')
        print("Response Status Code:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_project(self):  #Test creation of a new project.
        project_data = {
            'project_name': 'New Project',
            'client': self.client_instance.id,
            'users': [self.user.id]
        }
        response = self.client.post('/api/projects/', project_data, format='json')
        print("Response Data:", response.data)
        print("Response Status Code:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['project_name'], 'New Project')


    def test_list_projects(self):  # Test listing projects assigned to the logged-in user.
        self.client.force_authenticate(user=self.user)
        project = Project.objects.create(
            project_name='User Project',
            client=self.client_instance,
            created_by=self.user
        )
        project.users.set([self.user])

        # Test endpoint
        response = self.client.get('/api/projects/')
        print("Response Data:", response.data)
        print("Response Status Code:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['project_name'], 'User Project')

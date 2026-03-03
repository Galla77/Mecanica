from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from usuario.models import Usuario

class UsuarioAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testcliente',
            'email': 'cliente@test.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'Cliente',
            'rol': 'CLIENTE',
            'telefono': '123456789'
        }

    def test_crear_usuario(self):
        url = '/api/usuario/'
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Usuario.objects.filter(username='testcliente').exists())

    def test_obtener_token_jwt(self):
        # Primero crear el usuario
        Usuario.objects.create_user(username='testcliente', password='password123', email='cliente@test.com')
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testcliente', 'password': 'password123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_acceso_restringido(self):
        # Intentar ver la lista de usuarios sin estar autenticado
        url = '/api/usuario/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

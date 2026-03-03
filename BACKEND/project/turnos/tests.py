from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from usuario.models import Usuario
from turnos.models import Turno
import datetime

class TurnosAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cliente = Usuario.objects.create_user(username='cliente1', password='password123', rol='CLIENTE')
        self.admin = Usuario.objects.create_user(username='admin1', password='password123', rol='ADMIN')
        
    def test_crear_turno_como_cliente(self):
        self.client.force_authenticate(user=self.cliente)
        turno_data = {
            'nombre': 'Juan',
            'apellido': 'Perez',
            'marca': 'Ford',
            'modelo': 'Focus',
            'fecha': datetime.date.today().strftime('%Y-%m-%d'),
            'hora': '10:00:00',
            'descripcion': 'Cambio de aceite'
        }
        response = self.client.post('/api/turnos/', turno_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Turno.objects.count(), 1)
        # Verify it was assigned to cliente
        self.assertEqual(Turno.objects.first().usuario, self.cliente)

    def test_cliente_solo_ve_sus_turnos(self):
        self.client.force_authenticate(user=self.cliente)
        # Create one turn for cliente and one for admin
        Turno.objects.create(usuario=self.cliente, nombre='A', apellido='B', marca='C', modelo='D', fecha='2025-01-01', hora='10:00')
        Turno.objects.create(usuario=self.admin, nombre='E', apellido='F', marca='G', modelo='H', fecha='2025-01-02', hora='11:00')
        
        response = self.client.get('/api/turnos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['usuario'], self.cliente.id)

    def test_admin_ve_todos_los_turnos(self):
        self.client.force_authenticate(user=self.admin)
        Turno.objects.create(usuario=self.cliente, nombre='A', apellido='B', marca='C', modelo='D', fecha='2025-01-01', hora='10:00')
        Turno.objects.create(usuario=self.admin, nombre='E', apellido='F', marca='G', modelo='H', fecha='2025-01-02', hora='11:00')
        
        response = self.client.get('/api/turnos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

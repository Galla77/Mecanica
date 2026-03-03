import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from usuario.models import Usuario

if not Usuario.objects.filter(username='admin@mecanica.com').exists():
    Usuario.objects.create_superuser(
        username='admin@mecanica.com', 
        email='admin@mecanica.com', 
        password='adminpassword',
        rol='ADMIN',
        first_name='Administrador'
    )
    print("Cuenta ADMIN creada con exito.")
else:
    print("La cuenta ADMIN ya existe.")

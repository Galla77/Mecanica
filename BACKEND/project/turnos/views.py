from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Turno
from .serializers import TurnoSerializer
from .utils import send_turno_created_email, send_turno_updated_email

class TurnoViewSet(viewsets.ModelViewSet):
    serializer_class = TurnoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Admins and mechanics can see all appointments
        if user.rol in ['ADMIN', 'MECANICO']:
            return Turno.objects.all().order_by('-fecha', '-hora')
        
        # Customers can only see their own appointments
        return Turno.objects.filter(usuario=user).order_by('-fecha', '-hora')

    def perform_create(self, serializer):
        # Automatically set the appointment's user to the requesting user
        turno = serializer.save(usuario=self.request.user)
        send_turno_created_email(turno)
        
    def perform_update(self, serializer):
        # Record old instance
        old_turno = self.get_object()
        
        # Save modifications
        turno = serializer.save()
        
        # If any significant field changed, send update email
        if old_turno.estado != turno.estado or old_turno.fecha != turno.fecha or old_turno.hora != turno.hora:
            send_turno_updated_email(turno)

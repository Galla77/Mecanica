from django.core.mail import send_mail
from django.conf import settings

def send_turno_created_email(turno):
    subject = f"Confirmación de Solicitud de Turno - Mecánica Galla"
    message = (
        f"Hola {turno.nombre},\n\n"
        f"Hemos recibido tu solicitud de turno para tu {turno.marca} {turno.modelo}.\n"
        f"Fecha: {turno.fecha}\n"
        f"Hora: {turno.hora}\n"
        f"Estado actual: PENDIENTE\n\n"
        f"Un administrador revisará tu solicitud y te informaremos en caso de cambiar el estado a CONFIRMADO.\n\n"
        f"Saludos,\n"
        f"El equipo de Mecánica Galla"
    )
    
    if turno.usuario and turno.usuario.email:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[turno.usuario.email],
            fail_silently=True,
        )

def send_turno_updated_email(turno):
    subject = f"Actualización de tu Turno en Mecánica Galla"
    message = (
        f"Hola {turno.nombre},\n\n"
        f"Te informamos que ha habido una actualización en el turno solicitado para tu {turno.marca} {turno.modelo}.\n\n"
        f"Detalles actualizados:\n"
        f"- Estado: {turno.estado}\n"
        f"- Fecha: {turno.fecha}\n"
        f"- Hora: {turno.hora}\n\n"
        f"Si tienes dudas, por favor contacta con nosotros.\n\n"
        f"Saludos,\n"
        f"El equipo de Mecánica Galla"
    )
    
    if turno.usuario and turno.usuario.email:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[turno.usuario.email],
            fail_silently=True,
        )

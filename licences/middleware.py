from django.shortcuts import redirect
from django.utils import timezone
from licences.models import Licence  # Assurez-vous d'importer le modèle Licence

class LicenceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response

        response = self.get_response(request)
        return response

    def process_request(self, request):
        # Vérifiez si l'utilisateur est dans l'admin ou sur la page d'expiration de la licence
        if request.path.startswith('/admin') or request.path.startswith('/licences/licence-expiree/'):
            return None

        # Vérifiez si une licence active existe
        licence = Licence.objects.filter(active=True).first()
        if licence:
            # Vérifiez si la licence a expiré
            if licence.date_expiration < timezone.now():
                # Déactivez la licence et redirigez vers la page d'expiration de la licence
                licence.active = False
                licence.save()
                return redirect('licence_expiree')
        else:
            # Redirigez vers la page d'expiration de la licence si aucune licence active n'existe
            return redirect('licence_expiree')
        return None

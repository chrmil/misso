from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Supprime tous les utilisateurs de la base de données'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        count = User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'{count[0]} utilisateurs supprimés avec succès.'))
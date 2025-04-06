from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Historique

class HistoriqueTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password")
    
    def test_enregistrer_historique(self):
        Historique.objects.create(utilisateur=self.user, action="Test action")
        historique = Historique.objects.filter(utilisateur=self.user)
        self.assertEqual(historique.count(), 1)
        self.assertEqual(historique.first().action, "Test action")

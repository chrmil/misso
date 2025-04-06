# MiSSO - Site Web de Gestion et Visualisation

Ce projet est un site web développé avec Django pour la gestion et la visualisation des données liées aux objets connectés, événements, menus, et plus encore. Il inclut des fonctionnalités telles que la génération de rapports PDF, des graphiques interactifs, et un système d'historique des actions.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python 3.8 ou supérieur
- Pip (gestionnaire de paquets Python)

## Installation

1. Clonez ce dépôt sur votre machine locale :

```bash
git clone https://github.com/votre-utilisateur/misso.git
cd misso
```

2. Créez un environnement virtuel et activez-le :

```bash
python -m venv env
source env/bin/activate  # Sur Windows : env\Scripts\activate
```

3. Installez les dépendances nécessaires :

```bash
pip install django matplotlib reportlab
```

4. Appliquez les migrations pour configurer la base de données :

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Lancez le serveur de développement :

```bash
python manage.py runserver
```

6. Accédez au site web à l'adresse suivante :

[http://127.0.0.1:8000](http://127.0.0.1:8000)

# Fonctionnalités

- **Gestion des utilisateurs** : Inscription, connexion, déconnexion, et modification de profil.
- **Rapports graphiques** : Visualisation des données sous forme de graphiques interactifs.
- **Génération de PDF** : Téléchargez des rapports détaillés au format PDF.
- **Historique des actions** : Suivi des connexions, inscriptions, et autres actions utilisateur.
- **Gestion des objets connectés** : Activation, modification, et suivi des objets connectés.

# Dépendances principales

- **Django** : Framework web principal.
- **Matplotlib** : Génération de graphiques pour les rapports.
- **ReportLab** : Génération de fichiers PDF.

# Structure du projet

- ```utilisateurs/``` : Gestion des utilisateurs (inscription, connexion, profil, etc.).
- ```objets_connectes/``` : Gestion des objets connectés et rapports associés.
- ```evenements/``` : Gestion des événements et demandes.
- ```menu/``` : Gestion des menus et restaurants.
- ```historique/``` : Suivi des actions utilisateur.

# Commandes utiles

- Créer un superutilisateur pour accéder à l'interface d'administration :

```bash
python manage.py createsuperuser
# Pour créer un admin

python manage.py clear_users
#pour supprimer tous les utilisateurs
```

# Auteur

Ce projet a été développé par Christelle Millet, Eric Shao, Leon Chen, Aline Kim, Mattéo Manresa.

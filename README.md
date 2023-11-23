# UE-AD-A1-REST

Dans ce tp, nous avons développé 4 API REST en relation entre elles.
C'est uniquement sur l'API User que les utilisateurs pourront effectuer des requêtes.
L'API User aura, elle, accès à Movie et Booking. Enfin, Booking est également en relation avec Showtimes.
Pour avoir le détail de chacune des routes disponibles, un fichier YAML est disponible dans le dossier de chaque API, détaillant les fonctionnalités que celle-ci propose.

## API User

Cette API propose un accès à toutes les données relatives aux utilisateurs. Les données de la base sont de la forme :
- un identifiant
- un nom (Nom et Prénom)
- un indicateur de la dernière fois qu'il était actif

## API Movie

Cette API propose un accès à toutes les données relatives aux films dans la base de données. Les données sont de la forme :
 - identifiant d'un film
 - titre d'un film
 - nom du directeur d'un film
 - note donnée à un film

## API Booking

Cette API propose un accès à toutes les données relatives à la réservation de séances par les utilisateurs. Les données sont de la forme :
- l'identifiant d'un utilisateur
- une liste "dates" composée à la fois :
    - d'une date 
    - d'une liste de séances de films réservées pour date

## API Showtime

Cette API propose un accès à toutes les données relatives aux dates de projection des films. Les données sont de la forme :
- l'identifiant d'un utilisateur
- une liste "dates" composée à la fois :
    - d'une date 
    - d'une liste de séances de films réservées pour date

## Déploiement 

Nous allons démarrer chacun des services afin de pouvoir effectuer des requêtes sur chacun d'entre eux.

Pour assurer un environnement de développement isolé, nous allons avoir recours à l'utilisation d'un environnement virtuel (venv). Suivez ces étapes pour configurer et activer votre venv sur windows :

### Installation de virtualenv (si ce n'est pas déjà fait)

```
pip install virtualenv
```

### Création d'un environnement virtuel

L'installation peut prendre plusieurs dizaines de secondes.

```
# Assurez-vous d'être dans le répertoire de votre projet
cd chemin/vers/votre/projet

# Créez un environnement virtuel (que l'on nommera ici 'venv')
python -m venv venv
```

### Activation de l'environnement virtuel

Pour activer l'environnement virtuel, il faut vous assurer que votre ExecutionPolicy autorise l'exécution du fichier d'activation du venv.

Vous pouvez vérifier la valeur de l'ExecutionPolicy (souvent par défaut définie sur votre poste à 'Restricted') en tapant :
```
Get-ExecutionPolicy
```

Pour pouvoir activer l'environnement virtuel, il faudra la passer en Bypass.

```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass
```

Puis lancer l'activation du venv avec :
```
venv\Scripts\Activate
```

Une fois l'activation réussie, vous devriez voir à gauche de votre terminal l'indication '(venv)' précéder la ligne.

### Installation des dépendances du projet

Cette action peut prendre plusieurs secondes, le temps de télécharger toutes les librairies nécessaires pour faire tourner les API.

```# Installez les dépendances à partir du fichier requirements.txt
pip install -r requirements.txt
```

### Lancement des API REST

Lancez chacune des API REST du projet (spécifiées ci-dessus). Il faut toutes les lancer à la suite avant de commencer à effectuer des requêtes, car elles sont interconnectées sur certaines requêtes.

Pour cela, déplacez-vous dans le dossier de l'API que vous souhaitez démarrer, puis lancez le fichier python correspondant. Exemple pour User :

```
cd user
python user.py
```

Il faudra démarrer 3 onglets supplémentaires dans votre terminal pour lancer les 3 API restantes. Déplacez-vous à la racine du projet (voir commande ci-dessus) n'oubliez pas d'activer l'environnement virtuel (voir commande ci-dessus).
Ensuite, tapez dans chacun des terminaux les deux lignes de commandes juste au-dessus en remplaçant 'user' par :
- 'movie' la première fois
- 'showtime' la deuxième
- 'booking' dans le dernier onglet

Après ces étapes, les API REST devraient être accessibles.

### Fin d'utilisation
A la fin de l'utilisation des API, n'oubliez pas de vous déconnecter de l'environnement virtuel en tapant la commande :
```
deactivate
```

ainsi que de rétablir votre ExecutionPolicy par défaut : 

```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Default
```

Vous pouvez vérifier sa valeur si vous le souhaitez en tapant :
```
Get-ExecutionPolicy
```

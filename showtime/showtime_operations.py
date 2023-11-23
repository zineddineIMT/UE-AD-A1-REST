import json
from datetime import datetime


# Fonction pour charger les horaires des séances depuis un fichier JSON
def load_schedule():
    with open('./databases/times.json', "r") as jsf:
        return json.load(jsf)["schedule"]


# Chargement initial des horaires des séances
schedule = load_schedule()


# Renvoie la liste complète des horaires des séances
def get_schedule():
    return schedule


# Renvoie les séances pour une date donnée
def get_movies_by_date(date):
    try:
        # Validation du format de la date
        datetime.strptime(date, "%Y%m%d")
    except ValueError:
        # Renvoie une erreur si la date n'est pas dans le bon format
        return {"error": "Bad input parameter"}, 400

    # Recherche des séances planifiées pour la date donnée
    movies_for_date = next((item for item in schedule if item["date"] == date), None)
    if movies_for_date:
        # Renvoie les séances si elles sont trouvées
        return movies_for_date, 200
    else:
        # Renvoie une erreur si aucune séance n'est trouvée
        return {"error": "No movies scheduled for this date"}, 404

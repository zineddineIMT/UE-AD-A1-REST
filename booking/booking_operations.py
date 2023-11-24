import json
import requests
from datetime import datetime


# Fonction pour charger les réservations depuis un fichier JSON
def load_bookings():
    with open('./databases/bookings.json', "r") as jsf:
        return json.load(jsf)["bookings"]


# Initialisation des réservations
bookings = load_bookings()


def get_all_bookings():
    # Renvoie toutes les réservations chargées
    return bookings


def get_bookings_for_user(userid):
    # Filtrage des réservations par ID utilisateur
    user_bookings = [booking for booking in bookings if booking["userid"] == userid]
    # Renvoie les réservations trouvées ou un message d'erreur si aucune n'est trouvée
    return (user_bookings, 200) if user_bookings else ({"error": "No bookings found for this user"}, 404)


def add_booking_by_user(userid, booking_data):
    # Vérifie si les champs nécessaires sont présents dans les données de réservation
    if not booking_data or 'date' not in booking_data or 'movieid' not in booking_data:
        return {"error": "Invalid data format"}, 400

    # Vérifie le format de la date
    try:
        datetime.strptime(booking_data['date'], '%Y%m%d')
    except ValueError:
        return {"error": "Invalid date format"}, 400

    # Vérifie la disponibilité du film à la date donnée
    try:
        showtime_response = requests.get(f"http://localhost:3202/showmovies/{booking_data['date']}")
        if showtime_response.status_code != 200 or booking_data['movieid'] not in showtime_response.json()["movies"]:
            return {"error": "Movie not available on this date"}, 404
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

    # Vérifie si l'utilisateur a déjà une réservation pour cette date et ce film
    for booking in bookings:
        if booking['userid'] == userid:
            for d in booking['dates']:
                if d['date'] == booking_data['date']:
                    if booking_data['movieid'] in d['movies']:
                        return {"error": "An existing item already exists"}, 409

    # Ajoute la réservation pour un utilisateur existant ou crée une nouvelle entrée pour un nouvel utilisateur
    new_booking = {"date": booking_data['date'], "movies": [booking_data['movieid']]}
    existing_user = next((b for b in bookings if b["userid"] == userid), None)
    if existing_user:
        existing_user['dates'].append(new_booking)
    else:
        bookings.append({"userid": userid, "dates": [new_booking]})

    return booking_data, 200

import requests
import json


# Fonction pour charger les données des utilisateurs
def load_users():
    with open('./databases/users.json', "r") as jsf:
        return json.load(jsf)["users"]


users = load_users()


# Récupère les réservations d'un utilisateur
def get_user_bookings(userId):
    try:
        response = fetch_booking_data(userId)
        return response.json(), response.status_code
    except requests.RequestException as e:
        return {"error": str(e)}, 500


# Récupère les films réservés par un utilisateur
def get_user_booking_movies(userId):
    try:
        booking_response = fetch_booking_data(userId)
        if booking_response.status_code == 200:
            return extract_movie_details_from_bookings(booking_response.json()), 200
        else:
            return {"error": "User or booking not found"}, booking_response.status_code
    except requests.RequestException as e:
        return {"error": str(e)}, 500


# Ajoute une réservation pour un utilisateur
def add_booking_for_user(userId, booking_data):
    try:
        return send_booking_data(userId, booking_data)
    except requests.RequestException as e:
        return {"error": "Failed to connect to Booking service", "details": str(e)}, 500


# Fonctions auxiliaires pour simplifier la logique métier

def fetch_booking_data(userId):
    booking_service_url = f"http://localhost:3201/bookings/{userId}"
    return requests.get(booking_service_url)


def extract_movie_details_from_bookings(bookings_data):
    movie_details = []
    movie_service_url = "http://localhost:3200/movies/"
    for booking in bookings_data:
        for date in booking['dates']:
            for movie_id in date['movies']:
                movie_response = requests.get(f"{movie_service_url}{movie_id}")
                if movie_response.status_code == 200:
                    movie_details.append(movie_response.json())
    return movie_details


def send_booking_data(userId, booking_data):
    booking_service_url = f"http://localhost:3201/bookings/{userId}"
    booking_response = requests.post(booking_service_url, json=booking_data)
    if booking_response.status_code == 200:
        return booking_response.json(), 200
    else:
        return {"error": "Booking service responded with an error",
                "details": booking_response.json()}, booking_response.status_code

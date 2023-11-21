from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users/<userId>/bookings", methods=['GET'])
def getUserBookings(userId):
    # URL du service Booking
    booking_service_url = "http://localhost:3201/bookings/{}".format(userId)

    try:
        # Appel au service Booking
        response = requests.get(booking_service_url)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users/<userId>/bookings/movies", methods=['GET'])
def getUserBookingMovies(userId):
    # URL du service Booking
    booking_service_url = "http://localhost:3201/bookings/{}".format(userId)

    try:
        # Appel au service Booking
        booking_response = requests.get(booking_service_url)
        if booking_response.status_code == 200:
            bookings_data = booking_response.json()
            movie_details = []

            # URL de base du service Movie
            movie_service_url = "http://localhost:3200/movies/"

            for booking in bookings_data:
                for date in booking['dates']:
                    for movie_id in date['movies']:
                        # Appel au service Movie pour chaque ID de film
                        movie_response = requests.get(movie_service_url + movie_id)
                        if movie_response.status_code == 200:
                            movie_details.append(movie_response.json())

            return jsonify(movie_details), 200
        else:
            return jsonify({"error": "User or booking not found"}), 404
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/users/<userId>/bookings/add", methods=['POST'])
def addBookingForUser(userId):
    # Récupérer les données de la requête entrante
    booking_data = request.get_json()

    # URL du service Booking
    booking_service_url = "http://localhost:3201/bookings/{}".format(userId)

    try:
        # Envoyer les données de réservation au service Booking
        booking_response = requests.post(booking_service_url, json=booking_data)

        # Vérifier la réponse du service Booking
        if booking_response.status_code == 200:
            return jsonify(booking_response.json()), 200
        else:
            # Gérer les erreurs possibles du service Booking
            return jsonify({"error": "Booking service responded with an error",
                            "details": booking_response.json()}), booking_response.status_code
    except requests.RequestException as e:
        # Gérer les erreurs de connexion au service Booking
        return jsonify({"error": "Failed to connect to Booking service", "details": str(e)}), 500


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)

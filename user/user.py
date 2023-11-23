from flask import Flask, request, jsonify, make_response
import user_operations as uops

# Création de l'application Flask
app = Flask(__name__)

# Configuration du port et de l'hôte pour le serveur
PORT = 3203
HOST = '0.0.0.0'


# Route pour la page d'accueil
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


# Route pour obtenir les réservations d'un utilisateur
@app.route("/users/<userId>/bookings", methods=['GET'])
def get_user_bookings_route(userId):
    response, status_code = uops.get_user_bookings(userId)
    return make_response(jsonify(response), status_code)


# Route pour obtenir les films réservés par un utilisateur
@app.route("/users/<userId>/bookings/movies", methods=['GET'])
def get_user_booking_movies_route(userId):
    response, status_code = uops.get_user_booking_movies(userId)
    return make_response(jsonify(response), status_code)


# Route pour ajouter une réservation pour un utilisateur
@app.route("/users/<userId>/bookings/add", methods=['POST'])
def add_booking_for_user_route(userId):
    booking_data = request.get_json()
    response, status_code = uops.add_booking_for_user(userId, booking_data)
    return make_response(jsonify(response), status_code)


# Point d'entrée pour exécuter l'application Flask
if __name__ == "__main__":
    print(f"Server running in port {PORT}")
    app.run(host=HOST, port=PORT)

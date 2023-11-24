from flask import Flask, request, jsonify, make_response
import booking_operations as bops

# Initialisation de l'application Flask
app = Flask(__name__)

# Définition du port et de l'adresse hôte pour le serveur
PORT = 3201
HOST = '0.0.0.0'


# Route pour la page d'accueil
@app.route("/", methods=['GET'])
def home():
    # Renvoie un message de bienvenue
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


# Route pour obtenir toutes les réservations
@app.route("/bookings", methods=['GET'])
def get_all_bookings_route():
    # Utilise la fonction get_all_bookings pour récupérer les réservations
    return jsonify({"bookings": bops.get_all_bookings()})


# Route pour obtenir les réservations d'un utilisateur spécifique
@app.route("/bookings/<userid>", methods=['GET'])
def get_bookings_for_user_route(userid):
    # Récupère les réservations pour un utilisateur et renvoie une réponse adaptée
    user_bookings, status_code = bops.get_bookings_for_user(userid)
    return make_response(jsonify(user_bookings), status_code)


# Route pour ajouter une réservation pour un utilisateur
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_by_user_route(userid):
    # Récupère les données de réservation envoyées par l'utilisateur
    booking_data = request.get_json()
    # Ajoute la réservation et renvoie une réponse adaptée
    response, status_code = bops.add_booking_by_user(userid, booking_data)
    return make_response(jsonify(response), status_code)


# Point d'entrée principal pour exécuter l'application Flask
if __name__ == "__main__":
    # Affichage du port sur lequel le serveur est en cours d'exécution
    print(f"Server running in port {PORT}")
    # Démarrage du serveur Flask
    app.run(host=HOST, port=PORT)

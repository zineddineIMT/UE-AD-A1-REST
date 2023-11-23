# Importation des modules nécessaires pour Flask et des opérations de showtime
from flask import Flask, jsonify, make_response
import showtime_operations as sops

# Initialisation de l'application Flask
app = Flask(__name__)

# Définition du port et de l'adresse hôte pour le serveur
PORT = 3202
HOST = '0.0.0.0'


# Route pour la page d'accueil
@app.route("/", methods=['GET'])
def home():
    # Renvoie un message de bienvenue lorsque la route racine est demandée
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


# Route pour obtenir l'horaire complet des séances
@app.route("/showtimes", methods=['GET'])
def get_schedule_route():
    # Utilise la fonction get_schedule de showtime_operations pour obtenir l'horaire et renvoie les données au format JSON
    return jsonify({"schedule": sops.get_schedule()})


# Route pour obtenir les films programmés à une date spécifique
@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_by_date_route(date):
    # Obtient les films pour une date donnée et gère les codes d'état de réponse
    movies_for_date, status_code = sops.get_movies_by_date(date)
    return make_response(jsonify(movies_for_date), status_code)


# Point d'entrée principal pour exécuter l'application Flask
if __name__ == "__main__":
    # Affiche un message dans la console indiquant que le serveur fonctionne et sur quel port
    print(f"Server running in port {PORT}")
    # Démarrage du serveur Flask sur l'hôte et le port définis
    app.run(host=HOST, port=PORT)

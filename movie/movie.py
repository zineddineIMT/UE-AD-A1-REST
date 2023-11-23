# Importation des modules nécessaires depuis le framework Flask et le module movie_operations
from flask import Flask, request, jsonify, make_response
import movie_operations as mop

# Initialisation de l'application Flask
app = Flask(__name__)

# Définition du port et de l'adresse hôte pour le serveur
PORT = 3200
HOST = '0.0.0.0'


# Définition de la route racine et de la méthode GET pour afficher un message de bienvenue
@app.route("/", methods=['GET'])
def home():
    # Envoie une réponse HTTP avec un message de bienvenue
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


# Définition de la route pour obtenir tous les films avec la méthode GET
@app.route("/movies", methods=['GET'])
def get_all_movies_route():
    # Récupère tous les films à l'aide de la fonction définie dans movie_operations et envoie les données au format JSON
    return make_response(jsonify(mop.get_all_movies()), 200)


# Définition de la route pour obtenir un film par son ID avec la méthode GET
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_by_id_route(movieid):
    # Récupère un film par son ID et envoie la réponse correspondante
    movie, status_code = mop.get_movie_by_id(movieid)
    return make_response(jsonify(movie), status_code)


# Définition de la route pour obtenir les films par réalisateur avec la méthode GET
@app.route("/movies/director/<director>", methods=['GET'])
def get_movies_by_director_route(director):
    # Récupère les films d'un réalisateur spécifique et renvoie les données au format JSON
    movies, status_code = mop.get_movies_by_director(director)
    return make_response(jsonify(movies), status_code)


# Définition de la route pour obtenir un film par son titre avec la méthode GET
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_by_title_route():
    # Récupère un film par son titre en utilisant les paramètres de requête et envoie la réponse correspondante
    movie, status_code = mop.get_movie_by_title(request.args.get('title', ''))
    return make_response(jsonify(movie), status_code)


# Définition de la route pour ajouter un film avec la méthode POST
@app.route("/movies/<movieid>", methods=['POST'])
def add_movie_route(movieid):
    # Récupère les données JSON de la requête et ajoute un film, puis renvoie une réponse
    req = request.get_json()
    response, status_code = mop.add_movie(movieid, req)
    return make_response(jsonify(response), status_code)


# Définition de la route pour mettre à jour la note d'un film avec la méthode PUT
@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating_route(movieid, rate):
    # Met à jour la note d'un film et renvoie une réponse
    response, status_code = mop.update_movie_rating(movieid, rate)
    return make_response(jsonify(response), status_code)


# Définition de la route pour supprimer un film avec la méthode DELETE
@app.route("/movies/<movieid>", methods=['DELETE'])
def delete_movie_route(movieid):
    # Supprime un film par son ID et renvoie une réponse
    response, status_code = mop.delete_movie(movieid)
    return make_response(jsonify(response), status_code)


# Point d'entrée principal pour exécuter l'application Flask
if __name__ == "__main__":
    # Affiche un message indiquant que le serveur fonctionne et sur quel port
    print("Server running in port %s" % PORT)
    # Démarre le serveur sur l'hôte et le port définis
    app.run(host=HOST, port=PORT)

import json


# Fonction pour charger les données des films depuis un fichier JSON
def load_movies():
    with open('./databases/movies.json', "r") as jsf:
        # Retourne la liste des films chargée du fichier JSON
        return json.load(jsf)["movies"]


# Chargement initial des données des films au démarrage du module
movies = load_movies()


# Récupère et retourne la liste complète des films
def get_all_movies():
    return movies


# Recherche et retourne un film par son ID
def get_movie_by_id(movieid):
    # Utilise une compréhension de liste et next pour trouver le premier film correspondant, ou None si aucun n'est trouvé
    movie = next((movie for movie in movies if str(movie["id"]) == str(movieid)), None)
    # Retourne le film et un code de statut HTTP 200 si trouvé, sinon un message d'erreur et un code 404
    return (movie, 200) if movie else ({"error": "Movie ID not found"}, 404)


# Recherche et retourne les films par réalisateur
def get_movies_by_director(director):
    # Filtre les films dont le réalisateur correspond au paramètre, insensible à la casse
    matching_movies = [movie for movie in movies if movie['director'].lower() == director.lower()]
    # Retourne les films correspondants et un code 200, sinon un message d'erreur et un code 404
    return (matching_movies, 200) if matching_movies else ({"error": "No movies found for this director"}, 404)


# Recherche et retourne un film par son titre
def get_movie_by_title(title):
    # Même logique que get_movie_by_id, mais filtre par le titre du film
    movie = next((movie for movie in movies if movie["title"].lower() == title.lower()), None)
    return (movie, 200) if movie else ({"error": "Movie title not found"}, 404)


# Ajoute un nouveau film à la liste des films
def add_movie(movieid, movie_data):
    # Vérifie si un film avec le même ID existe déjà
    if any(movie["id"] == movieid for movie in movies):
        # Si un film existe déjà avec cet ID, retourne un message d'erreur et un code 409
        return ({"error": "Movie ID already exists"}, 409)
    # Ajoute le nouveau film à la liste et retourne un message de succès et un code 200
    movies.append(movie_data)
    return ({"message": "Movie added"}, 200)


# Met à jour la note d'un film existant
def update_movie_rating(movieid, rate):
    # Recherche le film par ID
    movie = next((movie for movie in movies if movie["id"] == movieid), None)
    if movie is None:
        # Si le film n'est pas trouvé, retourne un message d'erreur et un code 404
        return ({"error": "Movie ID not found"}, 404)
    # Met à jour la note du film et retourne le film mis à jour avec un code 200
    movie["rating"] = float(rate)
    return (movie, 200)


# Supprime un film de la liste par son ID
def delete_movie(movieid):
    global movies  # Déclare 'movies' comme global pour pouvoir modifier la liste originale
    movie = next((movie for movie in movies if movie["id"] == movieid), None)
    if movie is None:
        # Si le film n'est pas trouvé, retourne un message d'erreur et un code 404
        return ({"error": "Movie ID not found"}, 404)
    # Crée une nouvelle liste sans le film à supprimer et met à jour la liste des films
    movies = [m for m in movies if m["id"] != movieid]
    return ({"message": "Movie deleted"}, 200)

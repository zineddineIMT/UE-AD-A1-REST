from flask import Flask, render_template, request, jsonify, make_response
import json
from datetime import datetime
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/showtimes", methods=['GET'])
def get_schedule():
    # Renvoie la liste complète des horaires
    return jsonify({"schedule": schedule})

@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_bydate(date):
    try:
        # Validation de la date
        datetime.strptime(date, "%Y%m%d")
    except ValueError:
        # Si la date n'est pas valide, renvoie une erreur 400
        return make_response(jsonify({"error": "bad input parameter"}), 400)

    # Recherche des films pour la date donnée
    movies_for_date = next((item for item in schedule if item["date"] == date), None)
    if movies_for_date:
        return jsonify(movies_for_date)
    else:
        return make_response(jsonify({"error": "No movies scheduled for this date"}), 404)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)

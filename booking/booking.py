from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from datetime import datetime
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
    # Renvoie la liste complète des réservations
    return jsonify({"bookings": bookings})

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    user_bookings = []
    for booking in bookings:
        if booking["userid"] == userid:
            user_bookings.append(booking)

    if not user_bookings:
        return make_response(jsonify({"error": "No bookings found for this user"}), 404)

    return jsonify(user_bookings)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    booking_data = request.get_json()

    # Vérification de la structure et du format de données
    if not booking_data or 'date' not in booking_data or 'movieid' not in booking_data:
        return make_response(jsonify({"error": "Invalid data format"}), 400)

    # Vérification du format de la date
    try:
        datetime.strptime(booking_data['date'], '%Y%m%d')
    except ValueError:
        return make_response(jsonify({"error": "Invalid date format"}), 400)

    user_found = False
    date_already_booked = False

    # Parcourir les réservations pour vérifier si l'utilisateur et la date existent
    for booking in bookings:
        if booking['userid'] == userid:
            user_found = True
            for date in booking['dates']:
                if date['date'] == booking_data['date']:
                    date_already_booked = True
                    break
            if date_already_booked:
                break

    if date_already_booked:
        return make_response(jsonify({"error": "An existing item already exists"}), 409)

    # Ajout de la réservation pour un utilisateur existant ou un nouvel utilisateur
    if user_found:
        for booking in bookings:
            if booking['userid'] == userid:
                booking['dates'].append({"date": booking_data['date'], "movies": [booking_data['movieid']]})
                break
    else:
        new_user_booking = {
            "userid": userid,
            "dates": [{"date": booking_data['date'], "movies": [booking_data['movieid']]}]
        }
        bookings.append(new_user_booking)

    return jsonify(booking_data), 200

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)

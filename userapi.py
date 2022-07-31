# ----------------------------
# GAMESHARE User API
# Component Lead: Syed Safwaan
# ----------------------------

import datetime as dt
import json
from flask import Flask, request
from flask_cors import CORS
from firebase_admin import initialize_app, credentials, firestore

# Connect to Firestore db services
certs = credentials.Certificate('serviceAccountKey.json')
initialize_app(certs)
db = firestore.client()

# Set up Flask
app = Flask(__name__)
CORS(app)

required_fields = "firstName", "lastName"
optional_fields = "bio", "consoles", "sales", "rentals"


# ----- API FUNCTIONALITY
@app.route('/users', methods=['GET'])
def get_all_users():
    """ Returns all users in the Firestore 'users' collection. """
    data = db.collection('users').get()
    users = [doc.to_dict() for doc in data]
    return json.dumps(users, indent=4, sort_keys=True, default=str)


@app.route('/users/user/<uid>', methods=['GET'])
def get_user(uid):
    """ Returns user referenced by 'uid' in Firestore collection. """
    [data] = db.collection('users').where('uid', '==', uid).get()
    user = data.to_dict()
    return user


@app.route('/users/create/', methods=['POST'])
def create_user():
    """ Creates user with POST request data within Firestore collection. """
    form = request.form

    time = dt.datetime.now()
    user_data = {
        field: form[field] for field in required_fields
    } | {
        field: form.get(field, None) for field in optional_fields
    }

    _, doc = db.collection('users').add(user_data)  # initial data
    db.collection('users').document(doc.id).set({  # document-related data
        "uid": doc.id,
        "createDate": time,
        "updateDate": time
    })

    return "User successfully created", 201


@app.route('/users/update/<uid>', methods=['PATCH'])
def update_user():
    """ Updates user referenced by 'uid' within Firestore collection. """
    form = request.form

    time = dt.datetime.now()
    user_data = {
        field: form[field] for field in required_fields
    } | {
        field: form.get(field, None) for field in optional_fields
    }

    db.collection('users').document(form["uid"]).set(user_data | {"updateDate": time})
    return "User successfully updated", 200


@app.route('/users/delete', methods=['DELETE'])
def delete_user():
    """ Deletes user referenced by 'uid' within Firestore collection. """
    form = request.form
    uid = form["uid"]

    db.collection('users').document(uid).delete()
    return "User successfully deleted", 204


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)

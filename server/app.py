#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# View to get an earthquake by ID
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)
    if not earthquake:
        return make_response(jsonify({"message": f"Earthquake {id} not found."}), 404)
    
    response_body = {
        "id": earthquake.id,
        "location": earthquake.location,
        "magnitude": earthquake.magnitude,
        "year": earthquake.year
    }
    return make_response(jsonify(response_body), 200)

# New view to get all earthquakes with magnitude >= specified value
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # Query to find all earthquakes with magnitude >= specified value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Create a list of dictionaries containing earthquake details
    quakes_list = [
        {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }
        for quake in earthquakes
    ]

    # Prepare the response
    response_body = {
        "count": len(quakes_list),
        "quakes": quakes_list
    }
    return make_response(jsonify(response_body), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

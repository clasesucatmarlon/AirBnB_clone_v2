#!/usr/bin/python3
"""
List cities
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """ Tear down close storage
    """
    storage.close()


@app.route('/cities_by_states')
def cities_by_states():
    """ Display list cities
    """
    states = storage.all(State).values()

    return render_template('8-cities_by_states.html', list=states)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

#!/usr/bin/python3
"""
Write a script that starts a Flask web application:
Your web application must be listening on 0.0.0.0, port 5000
Routes:
/: display “Hello HBNB!”
/hbnb: display “HBNB”
/c/<text>: display “C ”, followed by the value of the text
variable (replace underscore _ symbols with a space)
/python/(<text>): display “Python ”, followed by the value of the text
variable (replace underscore _ symbols with a space)
The default value of text is “is cool”
/number/<n>: display “n is a number” only if n is an integer
"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """ Display the site index
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Display the site hbnb
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ Display the site with input value of variable
    """
    return "C " + text.replace("_", " ")


@app.route('/python/')
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """ Display the site index
    """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ Display the site number parameter
    """
    return "{} is a number".format(n)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

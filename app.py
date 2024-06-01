from flask import Flask

app = Flask(__name__)
app.secret_key = 'mysecret'

from home_route import *

if __name__ == "__main__":
    app.run(debug=True, port=4500)

    
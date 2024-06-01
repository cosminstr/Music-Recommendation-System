from flask import Flask

app = Flask(__name__)
app.secret_key = 'mysecret'

from home_route import *

# user's songs
songs_data_list: list = []

if __name__ == "__main__":
    app.run(debug=True, port=4500)

    
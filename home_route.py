from flask import render_template, request
from app import *

@app.route('/', methods=['GET', 'POST'])

def home():

    if request.method == 'POST':
        # TODO 
        pass
    else:
        return render_template('index.html')
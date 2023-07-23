import os
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/word-clouds')
def word_clouds():
    return render_template('word-clouds.html')

@app.route('/word-data')
def word_data():
    return render_template('word-data.html')

@app.route('/prediksi')
def prediksi():
    return render_template('prediksi.html')

if __name__ == '__main__':
    app.run()

from flask import Flask, render_template

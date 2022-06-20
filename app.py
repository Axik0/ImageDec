from flask import Flask, render_template, request, url_for, flash, redirect
from flask_bootstrap import Bootstrap

from iprocess import image_process


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzzz'
Bootstrap(app)


@app.route("/")
def index():
    return render_template("index.html")


palette10c = ['#fec5bb', '#fcd5ce', '#fae1dd', '#f8edeb', '#e8e8e4', '#d8e2dc', '#ece4db', '#ffe5d9', '#ffd7ba', '#fec89a']


@app.route("/result")
def result():
    return render_template("result.html", hex_palette=palette10c, ahex_palette=palette10c)


if __name__ == '__main__':
    app.run()
    debug=True

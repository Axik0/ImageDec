from flask import Flask, render_template, request, url_for, flash, redirect
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from iprocess import fetch_process
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzzz'
Bootstrap(app)

app.config['UPLOAD_FOLDER'] = 'static/temp'
app.config['MAX_CONTENT_LENGTH'] = 1000*1000*10
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def is_allowed(filename):
    # we check that there is some filename (dot condition) and it's allowed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


img_path = None


@app.route("/", methods=['GET', 'POST'])
def index():
    global img_path
    if img_path:
        try:
            # remove previous file from temp folder by its path
            os.remove(img_path)
        except:
            flash("previous temp file doesn't exist or hasn't been removed", 'error')
    if request.method == 'POST':
        f = request.files['file']
        if f.filename != '':
            if is_allowed(f.filename):
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
                f.save(img_path)
                flash('file uploaded successfully', 'info')
                return redirect(url_for('result'))
            else:
                flash('incorrect file', 'error')
        else:
            flash('No selected file', 'error')
    return render_template("index.html")


# palette10c = ['#fec5bb', '#fcd5ce', '#fae1dd', '#f8edeb', '#e8e8e4', '#d8e2dc', '#ece4db', '#ffe5d9', '#ffd7ba', '#fec89a']


@app.route("/result")
def result():
    try:
        hex_palette_10c = fetch_process(img_path, advanced=True)
    except:
        flash('Processing error', 'error')
    return render_template("result.html", hex_palette=hex_palette_10c, image_path=img_path)


if __name__ == '__main__':
    app.run()
    debug = True

from flask import Flask, request, render_template, session, redirect, url_for
import pandas as pd
import os
import sys

app = Flask(__name__)

app.secret_key = os.urandom(28)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'), sep=';')
        shape = df.shape
        print(shape[0])
        session["data"] = df.to_json()
        print(sys.getsizeof(session["data"]))
        return render_template('upload.html', shape=df.shape,
                               tables=[df.to_html(classes='data')],
                               titles=df.columns.values)
    return render_template('upload.html')

@app.route("/step1", methods=['GET', 'POST'])
def step1():
    data = session.get('data')
    df = pd.read_json(data, dtype=False)
    return render_template('simple.html', shape=df.shape,
                           tables=[df.to_html(classes='data')],
                           titles=df.columns.values)
#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
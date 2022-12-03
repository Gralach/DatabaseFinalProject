# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, render_template, request
import joblib
import tensorflow as tf
from keras.models import load_model

app = Flask(__name__)

def checking(username, password):
    conn = sqlite3.connect('sqlite')
    localhost_save_option = tf.saved_model.LoadOptions(experimental_io_device="/job:localhost")
    model = joblib.load('model/pipe_lstm.joblib')
    model.named_steps['classifier'].model_ = load_model('model/lstm.h5', options=localhost_save_option)
    is_malicious = 'Malicious' in model.predict([username, password], verbose=0)
    try:
        if conn.execute(''' SELECT * FROM Blacklist WHERE text = "{}" OR text = "{}"'''.format(username, password)).fetchone() or is_malicious:
            # kalo salah satu input malicious
            result = "REJECT USER INPUT"
     
        else:
            if not conn.execute(''' SELECT * FROM Users WHERE username = "{}" AND password = "{}"'''.format(username, password)).fetchone():  # An empty result evaluates to False.
                result = "WRONG USERNAME OR PASSWORD"
            else:
                result = "LOGGED IN!"
    except:
        result = "INPUT INVALID"
    conn.close()
    return result

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        username = request.form['username']
       	password = request.form['password']
        result = checking(username, password)
        return result
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
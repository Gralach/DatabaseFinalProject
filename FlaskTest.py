# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, session
import joblib
import tensorflow as tf
from keras.models import load_model

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def checking(username, password):
    conn = sqlite3.connect('sqlite')
    localhost_save_option = tf.saved_model.LoadOptions(experimental_io_device="/job:localhost")
    model = joblib.load('model/pipe_lstm.joblib')
    model.named_steps['classifier'].model_ = load_model('model/lstm.h5', options=localhost_save_option)
    is_malicious = 'Malicious' in model.predict([username, password], verbose=0)
    check_blacklist = conn.execute(''' SELECT * FROM Blacklist WHERE text = "{}" OR text = "{}"'''.format(username, password)).fetchone()
    check_users = conn.execute(''' SELECT * FROM Users WHERE username = "{}" AND password = "{}"'''.format(username, password)).fetchone()
    try:
        if check_blacklist or is_malicious:
            # kalo salah satu input malicious
            result = "User Input Rejected or Malicious Detected"
     
        else:
            if not check_users:  # An empty result evaluates to False.
                result = "Username or Password is Wrong"
            else:
                result = check_users
    except:
        result = "Invalid Input"
    conn.close()
    return result

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        result = checking(username, password)
        if(username == result[1]):
            return render_template('output.html',result="Welcome, " + result[1])
        else:
            flash(result)
            return redirect(request.url)
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
import json
import random
import sys
from collections import Counter
from pprint import pprint
from flask import (Flask, flash, jsonify, logging, redirect, render_template,
                   request, session, url_for)
#from flask_mysqldb import MySQL
# from forms import PostForm, RegisterForm
# from passlib.hash import sha256_crypt
from utils import parseme

app = Flask(__name__)



@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))

    
    return render_template('index.html')

# User signup
@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        # Get form feilds
        adhaar = request.form['adhaar']
        #dob = request.form['dob']
     

        session['logged_in'] = True
        session['username'] = adhaar

        flash('You can now vote!', 'success')
        return redirect(url_for('dashboard'))


    return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Get form feilds
        username = request.form['username']
        password_candidate = request.form['password']
     

        session['logged_in'] = True
        session['username'] = username

        flash('You are now logged in', 'success')
        return redirect(url_for('dashboard'))


    return render_template('login.html')

#Dashboard routes
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' in session:

        myuser = {"first_name":"sadf", "last_name":"sadf", "roll_no":"123", "email":"sadf@asdf.com", "d_name":"dsadf"}

        candidates = [{"id":1, "name":"xyz", "party":"abc", "thumb":"https://qph.fs.quoracdn.net/main-qimg-aefe19660cb326f3679e526f4bf7ac0a"},
                        {"id":2, "name":"xyz", "party":"abc", "thumb":"https://qph.fs.quoracdn.net/main-qimg-aefe19660cb326f3679e526f4bf7ac0a"},
                        {"id":3, "name":"xyz", "party":"abc", "thumb":"https://qph.fs.quoracdn.net/main-qimg-aefe19660cb326f3679e526f4bf7ac0a"},
                        {"id":4, "name":"xyz", "party":"abc", "thumb":"https://qph.fs.quoracdn.net/main-qimg-aefe19660cb326f3679e526f4bf7ac0a"}
                        ]

        return render_template('dashboard.html', candidates=candidates, myuser=myuser)
    else:
        flash('You need to be logged in to access!', 'danger')
        return redirect(url_for('login'))


# Explore page routes
@app.route('/explore', methods=['GET', 'POST'])
def explore():
    if 'logged_in' in session:

        return render_template('explore.html')        

        if request.method == 'POST':
            print("jsonify?")
            return jsonify({"data":"pass"})
            # return jsonify({"data":data, "my_pids": my_pids})

        if request.method =='GET':
            return render_template('explore.html')
    else:
        flash('You need to be logged in to access!', 'danger')
        return redirect(url_for('login'))


@app.route('/add_bookmark', methods=['GET', 'POST'])
def add_bookmark():
    form = PostForm(request.form)
    if  request.method == 'POST' and form.validate():
        url = form.url.data
        cat = form.cat.data

        try:
            return redirect(url_for('dashboard'))

        except:
            flash("gg", 'danger')
            return render_template('add_bookmark.html', form=form)

    return render_template('add_bookmark.html', form=form)


@app.route('/myaccount', methods=['GET'])
def myaccount():
    if 'logged_in' in session:
        '''
        stats = {"total" : len(mybookmarks),
                 "unread" : len(mybookmarks) - unread,
                 "archived": unread,
                 }
        '''

        myuser = {"first_name":"sadf", "last_name":"sadf", "roll_no":"123", "email":"sadf@asdf.com", "d_name":"dsadf"}

        stats = {"total" : 5,
                 "unread" : 10,
                 "archived": 2,
                 }

        #return render_template('myaccount.html')
        return render_template('myaccount.html', myuser=myuser, stats=stats)

    else:
        flash('You need to be logged in to access!', 'danger')
        return redirect(url_for('login'))

@app.route('/archive-toggle', methods=['POST'])
def archive():   
    return jsonify({"data":"pass"})

# Data request for doughnut chart comes here
@app.route('/get-pie-data', methods=['GET'])
def getpiedata ():

    data = [{"category":"A", "count":5}, {"category":"B", "count":10}, {"category":"C", "count":6}]

    return jsonify({"data":data})

# Route for adding bookmark from the Explore page
@app.route('/add-mybookmark', methods=['POST'])
def addmybookmark():
    return jsonify({"data":"pass"})


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/vote', methods=['GET','POST'])
def add_message():
    data = request.json["b_id"]
    print(data)
    return jsonify({"data": data})


if __name__ =="__main__":
    app.secret_key = 'secret123'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="localhost", debug=True, threaded=True)

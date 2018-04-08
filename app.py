import json
import random
import sys
from collections import Counter
from pprint import pprint
from flask import (Flask, flash, jsonify, logging, redirect, render_template,
                   request, session, url_for)
from flask_mysqldb import MySQL
# from forms import PostForm, RegisterForm
# from passlib.hash import sha256_crypt
from utils import parseme
from solc import compile_source
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

app = Flask(__name__)

# Enter this information
HOST = "localhost"
USERNAME ="root" # change to your username and password
PASSWORD = "appu" #Kernelpanic

app.config['MYSQL_HOST'] = HOST
app.config['MYSQL_USER'] = USERNAME
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = 'codefundo'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL_DB
mysql = MySQL(app)

http_provider = HTTPProvider('http://localhost:8545')
eth_provider = Web3(http_provider).eth

default_account = eth_provider.accounts[0]

transaction_details = {
    'from': default_account,
}

with open('Vote.sol') as file:
    source_code = file.readlines()

# compile the contract
compiled_code = compile_source(''.join(source_code))

contract_name = 'Vote'

contract_bytecode = compiled_code["<stdin>:Vote"]['bin']
contract_abi = compiled_code["<stdin>:Vote"]['abi']


# create a contract factory. we'll use this to deploy any number of
# instances of the contract to the chain
contract_factory = eth_provider.contract(
    abi=contract_abi,
    bytecode=contract_bytecode,
)


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
        dob = request.form['dob']
     
        cur = mysql.connection.cursor()
        cur.execute("""SELECT
                        *
                        FROM voters                        
                        WHERE u_id=\'{}\';""".format(adhaar))

        data = list(cur.fetchall())
        cur.close()

        if(len(data)==0):
            cur = mysql.connection.cursor()
            cur.execute("""INSERT INTO
                        voters
                        (u_id, voted)
                        VALUES
                        ({0},1);""".format(adhaar))

            cur.close()

            mysql.connection.commit()

        else:
            flash('You have already voted!', 'danger')
            return redirect(url_for('register'))

        session['logged_in'] = True
        session['username'] = adhaar

        flash('You can now vote!', 'success')
        return redirect(url_for('dashboard'))


    return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('transactions'))

    if request.method == 'POST':
        # Get form feilds
        username = request.form['username']
        password_candidate = request.form['password']
     

        session['logged_in'] = True
        session['username'] = username
        session['admin'] = True

        flash('You are now logged in', 'success')
        return redirect(url_for('transactions'))


    return render_template('login.html')

#Dashboard routes
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' in session:

        myuser = {"first_name":"sadf", "last_name":"sadf", "roll_no":"123", "email":"sadf@asdf.com", "d_name":"dsadf", "constituency":"Mangaluru"}

        cur = mysql.connection.cursor()
        cur.execute("""SELECT
                        c_id,
                        name,
                        party,
                        constituency,
                        thumb
                        FROM candidates                        
                        WHERE constituency=\'{}\';""".format(myuser["constituency"]))

        candidates = list(cur.fetchall())
        cur.close()

        # candidates = [{"id":1, "name":"A", "party":"abc", "thumb":"https://qph.fs.quoracdn.net/main-qimg-aefe19660cb326f3679e526f4bf7ac0a"},
        #                 {"id":2, "name":"B", "party":"abc", "thumb":"https://qph.fs.quoracdn.net/main-qimg-aefe19660cb326f3679e526f4bf7ac0a"},
        #                 {"id":3, "name":"C", "party":"abc", "thumb":"https://qph.fs.quoracdn.net/main-qimg-aefe19660cb326f3679e526f4bf7ac0a"},
        #                 {"id":4, "name":"B", "party":"abc", "thumb":"https://qph.fs.quoracdn.net/main-qimg-aefe19660cb326f3679e526f4bf7ac0a"}
        #                 ]

        return render_template('dashboard.html', candidates=candidates, myuser=myuser)
    else:
        flash('You need to be logged in to access!', 'danger')
        return redirect(url_for('login'))

@app.route('/vote', methods=['GET','POST'])
def vote():
    print(request.json["candidate"])
    [candidate, c_id] = request.json["candidate"].split("-")
    constituency = request.json["constituency"]
    print(candidate, constituency)

    transaction_hash = contract_factory.constructor(
                            constituency.encode(), candidate.encode()).transact(transaction=transaction_details)

    transaction_receipt = eth_provider.getTransactionReceipt(transaction_hash)
    contract_address = transaction_receipt['contractAddress']

    #TODO Add transaction address with timestamp into DB with candidate foreign key

    cur = mysql.connection.cursor()
    cur.execute("""INSERT 
                    INTO 
                    transactions
                    (c_id, t_id, stamp) 
                    VALUES({0}, \'{1}\', NOW());""".format(c_id, contract_address))

    cur.close();

    mysql.connection.commit()    

    return jsonify({"address": contract_address})

@app.route('/transactions', methods=['GET','POST'])
def transactions():
    if  request.method == 'POST':
        # Asking for sepcific candidates transactions
        candidate = request.json("candidate")

        #TODO Query db for candidates transactions
        transactions = False
    
    else:
        # GET REQUEST
        cur = mysql.connection.cursor()
        cur.execute("""SELECT
                        DATE_FORMAT(stamp, '%d/%m/%Y %H:%i:%S') AS timestamp,
                        t_id
                        FROM transactions
                        ORDER BY stamp DESC;""")

        transactions = list(cur.fetchall())
        cur.close()
    
    return render_template('ledger.html', transactions=transactions)

@app.route('/ledger', methods=['GET', 'POST'])
def ledger():
    if request.method == 'POST':
        address = request.json["address"]
        # cur = mysql.connection.cursor()
        # cur.execute("""SELECT
        #                 name,
        #                 constituency
        #                 FROM candidates C JOIN transactions T
        #                 ON C.c_id=T.c_id                      
        #                 WHERE t_id=\'{}\';""".format(address))

        # candidate = list(cur.fetchall())[0]
        # cur.close()
        contract_instance = eth_provider.contract(
                                abi=contract_abi,
                                address=address,
                                ContractFactoryClass=ConciseContract
                                )
        constituency, candidate = contract_instance.info()
        return jsonify({"name":candidate.decode(), "constituency":constituency.decode()})

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
    return redirect(url_for('register'))


if __name__ =="__main__":
    app.secret_key = 'secret123'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="localhost", debug=True, threaded=True)

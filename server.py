from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
import md5
app = Flask(__name__)
mysql = MySQLConnector(app, 'loginAndRegistration')
app.secret_key = "This is a secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    # user_id = query
    # if "user_id" not in session:
    #     session['user_id'] = query
    return render_template("index.html")

@app.route('/success') 
def success():
    return render_template("success.html")

@app.route('/register', methods=['POST']) 
def register():
    if len(request.form['first_name']) < 2:
        flash("Name must be at least 2 characters!")
        return redirect ('/')
    elif request.form['first_name'].isalpha() == False: 
        flash("Name must contain letters only!")
        return redirect ('/')
    elif len(request.form['last_name']) < 2:
        flash("Name must be at least 2 characters!")
        return redirect ('/')
    elif request.form['last_name'].isalpha() == False: 
        flash("Name must contain letters only!")
        return redirect ('/')        
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Please enter a valid email address")
        return redirect ('/')        
    elif request.form['password'] != request.form['password_conf'] :
        flash("Passwords must match!") 
        return redirect ('/')         
    else:      
        query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': md5.new(request.form['password']).hexdigest()
        }
        mysql.query_db(query, data)
        return redirect('/success')

@app.route('/login', methods=['POST']) 
def login():
        
    query = "SELECT id FROM users WHERE email = :email AND password = :password"
    data = {
        'email': request.form['email'],
        'password': md5.new(request.form['password']).hexdigest()
    }

    user_id = mysql.query_db(query, data)
    if user_id == []:
        flash("Invalid email or password!")
        return redirect ('/')
    session['user_id'] = user_id 
    return redirect('/success')

@app.route('/logout', methods=['POST'])
def logout():

    session.clear()
    return redirect('/')


app.run(debug=True)   
     

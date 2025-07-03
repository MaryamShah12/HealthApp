import bcrypt
from flask import Flask, redirect, render_template, request, url_for, session
import mysql.connector

app = Flask(__name__)  # Fixed from '__name__' to __name__
app.secret_key = 'your_secret_key_here'  # Replace with a secure random string in production

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'healthapp'
}

@app.route('/')
def loginpage():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template("login.html", error=None)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return render_template('login.html', error='Password does not match!')
    
    pass_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, pass_hash))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('loginpage'))
    except mysql.connector.Error as err:
        if err.errno == 1062:
            error_msg = 'Username or email already exists'
        else:
            error_msg = "An error occurred: " + str(err)
        cursor.close()
        conn.close()
        return render_template('login.html', error=error_msg)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
            session['user_id'] = result[0]  # Store the user_id in session
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid username or password")
    except mysql.connector.Error as err:
        return render_template('login.html', error="An error occurred: " + str(err))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('loginpage'))
    return render_template('dashboard.html')

@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if 'user_id' not in session:
        return redirect(url_for('loginpage'))
    if request.method == 'POST':
        data_type = request.form['type']
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            if data_type == 'meals':
                query = "INSERT INTO meals (user_id, food_name, calories, carbs, protein, fat, timestamp) VALUES (%s, %s, %s, %s, %s, %s, NOW())"
                cursor.execute(query, (session['user_id'], request.form['food_name'], request.form['calories'], request.form['carbs'], request.form['protein'], request.form['fat']))
            elif data_type == 'exercise':
                query = "INSERT INTO exercise (user_id, activity, duration_mins, calories_b, timestamp) VALUES (%s, %s, %s, %s, NOW())"
                cursor.execute(query, (session['user_id'], request.form['activity'], request.form['duration_mins'], request.form['calories_burned']))
            elif data_type == 'sleep':
                query = "INSERT INTO sleep (user_id, hours, quality_rating, date) VALUES (%s, %s, %s, NOW())"
                cursor.execute(query, (session['user_id'], request.form['hours'], request.form['quality_rating']))
            elif data_type == 'water':
                query = "INSERT INTO water (user_id, amount_ml, timestamp) VALUES (%s, %s, NOW())"
                cursor.execute(query, (session['user_id'], request.form['liters']))
            elif data_type == 'mood':
                query = "INSERT INTO mood (user_id, rating, note, date) VALUES (%s, %s, %s, NOW())"
                cursor.execute(query, (session['user_id'], request.form['rating'], request.form['note']))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))
        except mysql.connector.Error as err:
            cursor.close()
            conn.close()
            return render_template('add_data.html', error="An error occurred: " + str(err))
    return render_template('add_data.html', error=None)

@app.route('/graphs')
def graphs():
    if 'user_id' not in session:
        return redirect(url_for('loginpage'))
    return render_template('graphs.html', error=None)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user_id from session, None if not present
    return redirect(url_for('loginpage'))

if __name__ == '__main__':
    app.run(debug=True)
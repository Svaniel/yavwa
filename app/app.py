from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# database configuration
db = mysql.connector.connect(
    host='db',
    user='myuser',
    password='mypassword',
    database='mydatabase'
)

# create user table
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")


@app.route('/')
def home():
    if 'user_id' in session:
        # Query the database for the user's profile
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
        user = cursor.fetchone()
        cursor.close()
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if the email is already in use
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user:
            flash('Email is already in use.')
            return redirect(url_for('register'))

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, password))
        db.commit()
        cursor.close()

        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the form data
        name = request.form['username']
        password = request.form['password']

        # Query the database for the user with the matching email and password
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE name = %s AND password = %s', (name, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Set the user_id in the session
            session['user_id'] = user[0]
            flash('Login successful.')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/profile')
def profile():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Retrieve user data from database
    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()

    # Render profile template with user data
    return render_template('profile.html', user=user)

@app.route('/settings/<int:id>', methods=['GET', 'POST'])
def settings(id):
    if request.method == 'POST':
        email = request.form['email']
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (email) VALUES (%s) WHERE id = %s", (email, id))
        db.commit()
        return redirect(url_for('profile'))
    
    cursor = db.cursor()
    cursor.execute("SELECT * from users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        return render_template('settings.html', user=user)
    else:
        return "User not found"


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

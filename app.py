from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secretkey'

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT, theater TEXT,
        timing TEXT, date TEXT, persons INTEGER, seats TEXT, movie TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Signup successful!')
            return redirect(url_for('home'))
        except:
            flash('Username already exists')
        conn.close()
    return render_template('signup.html')

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/book/<movie>')
def book(movie):
    return render_template('bookings.html', movie=movie)

# @app.route('/confirm', methods=['POST'])
# def confirm():
#     data = request.form
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''INSERT INTO bookings (name, phone, theater, timing, date, persons, seats, movie)
#                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
#                    (data['name'], data['phone'], data['theater'], data['timing'],
#                     data['date'], data['persons'], data['seats'], data['movie']))
#     conn.commit()
#     conn.close()
#     flash('Booking successful!')
#     return render_template('confirmation.html', booking=data)
@app.route("/confirm", methods=["POST"])
def confirm():
    data = request.form
    booking = {
        "name": data["name"],
        "phone": data["phone"],
        "movie": data["movie"],
        "theater": data["theater"],
        "timing": data["timing"],
        "date": data["date"],
        "persons": int(data["persons"]),
        "seats": data["seats"]
    }

    # Insert into SQLite
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO bookings (name, phone, movie, theater, timing, date, persons, seats)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (booking["name"], booking["phone"], booking["movie"], booking["theater"],
          booking["timing"], booking["date"], booking["persons"], booking["seats"]))
    conn.commit()
    conn.close()

    return render_template("confirmation.html", booking=booking)
@app.route("/admin/bookings")
def view_bookings():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    rows = c.fetchall()
    conn.close()
    return render_template("view_bookings.html", bookings=rows)


if __name__ == '__main__':
    app.run(debug=True)
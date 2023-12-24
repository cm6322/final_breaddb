from flask import Flask, jsonify, redirect, request, render_template, session, url_for
from flask_mysqldb import MySQL
from database import set_connector

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'appalling-antique-antelope'

# Required
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "breaddb"
# Extra configs
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_AUTOCOMMIT"] = True

mysql = MySQL(app)
set_connector(mysql)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register_page")
def register_page():
    return render_template('register.html')

@app.route("/rolls_edit_page")
def edit_page():
    username = session.get('username')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    if user:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM rolls WHERE user_id = %s", (user['id'],))
        rolls_data = cur.fetchone()
        cur.close()
        if rolls_data:
            return render_template("edit_rolls.html", rolls_data=rolls_data, username=username)
        else:
            return render_template("edit_rolls.html", username=username)

@app.route("/form_login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    if user:
        session['username'] = username
        return redirect(url_for("home"))
    else:
        error_message = "Invalid credentials. Please try again."
        return render_template("index.html", error=error_message)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/home', methods=['GET'])
def home():
    username = session.get('username')
    if username == "admin":
        return render_template('admin_home.html', username=username)
    else:
        print("User logged in successfully")
        return render_template('home.html', username=username) 

@app.route('/form_register', methods=['GET', 'POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    if user:
        error_message = "Username already exists. Please try again."
        return render_template("index.html", error=error_message)
    else:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("index"))

@app.route("/rolls")
def rolls():
    username = session.get('username')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    if user:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM rolls WHERE user_id = %s", (user['id'],))
        rolls_data = cur.fetchone()
        cur.close()
        if rolls_data:
            return rolls_counter()
        else:
            return render_template("rolls.html", rolls_data=rolls_data, username=username)
    return rolls_counter()

@app.route("/rolls_counter")
def rolls_counter():
    username = session.get('username') 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM rolls WHERE user_id = %s", (user['id'],))
        rolls_data = cur.fetchone()
        cur.close()
        return render_template("rolls.html", rolls_data=rolls_data, username=username)
    else:
        return "User not logged in"
    
@app.route("/create_rolls", methods=["POST"])
def create_rolls():
    username = session.get('username') 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    user_id = user['id']
    cur.execute("SELECT * FROM rolls WHERE user_id = %s", (user_id,))
    rolls_data = cur.fetchone()

    if not rolls_data:
        cur.execute("INSERT INTO rolls (user_id) VALUES (%s)", (user_id,))
        mysql.connection.commit()
        cur.close()
        return redirect("/rolls_counter")
    else:
        cur.close()
        return redirect("/rolls_counter")

@app.route("/edit_rolls", methods=["POST"])
def edit_rolls():
    username = session.get('username')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user:
        tix_10 = request.form.get("tix_10")
        tix_1 = request.form.get("tix_1")
        gems = request.form.get("gems")

        user_id = user['id']
        cur.execute("UPDATE rolls SET tix_10 = %s, tix_1 = %s, gems = %s WHERE user_id = %s",
                    (tix_10, tix_1, gems, user_id))
        mysql.connection.commit()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM rolls WHERE user_id = %s", (user_id,))
        rolls_data = cur.fetchone()
        cur.close()
        return render_template("edit_success.html", rolls_data=rolls_data, username=username)
    else:
        return "Edit failed."
    
@app.route("/rolls_data")
def view_all_rolls_data():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM GetAllRollsData")
        rolls_data = cur.fetchall()
        cur.close()

        rolls_data = [roll for roll in rolls_data if roll['user_id'] != 1]

        return render_template('view_rolls.html', rolls_data=rolls_data)
    except Exception as e:
        return str(e)

@app.route('/delete_user', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        
        cur = mysql.connection.cursor()
        cur.callproc('DeleteUserWithRollsData', [user_id])
        
        while cur.nextset():
            pass
        
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('view_all_rolls_data'))
    
if __name__ == "__main__":
    app.run(debug=True)
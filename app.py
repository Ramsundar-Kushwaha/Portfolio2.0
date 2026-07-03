from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
import mysql.connector

#load environment variables
load_dotenv()

#create flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

#database connection function
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )

#home Page
@app.route("/")
def home():
    return render_template("index.html")

#show projects (Dynamically)
@app.route("/projects")
def projects():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM projects"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("projects.html", projects = data)


# admin page and form
@app.route("/admin", methods=["GET", "POST"])
def adminLogin():

    # for GET method
    if request.method == "GET":
        return render_template("admin.html")
    

    # for POST method
    admin_id = request.form["admin_id"]
    admin_name = request.form["admin_name"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM admin WHERE id = %s AND name = %s"
    cursor.execute(query, (admin_id, admin_name,))

    admin = cursor.fetchone()

    # if authorized user (admin)
    if admin:
        session["admin_id"] = admin_id # building session

        cursor.close()
        conn.close()

        return redirect(url_for("dashBoard"))
    
    # if unauthorized user (unknown user)
    cursor.close()
    conn.close()
    return render_template("admin.html", error = "Invalid admin")


# dash board
@app.route("/dashboard")
def dashBoard():

    # if not logged in as admin
    if "admin_id" not in session:
        return redirect(url_for("adminLogin"))
    
    # if loogged in as admin
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT title FROM projects ORDER BY title DESC"
    cursor.execute(query)
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template("dashboard.html", projects = data)


# route for adding projects
@app.route("/addprojects", methods=["POST"])
def add_project():
    if "admin_id" not in session:
        return redirect(url_for("adminLogin"))
    
    title = request.form["title"]
    description = request.form["desc"]

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO projects (title, descriptions) VALUES (%s, %s)"

    cursor.execute(query, (title, description))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("dashBoard"))

# logout system
@app.route("/logout")
def logOut():
    session.clear()
    return redirect(url_for("adminLogin"))


# Run App
if __name__ == "__main__":
    app.run(debug=True, port=3000)
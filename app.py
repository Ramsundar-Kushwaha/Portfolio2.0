from flask import Flask, render_template, request, redirect
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
        port=int(os.getenv("DB_PORT", 3306))
    )

#Home Page
@app.route("/")
def home():
    return render_template("index.html")

#show projects (Dynamic)
@app.route("/projects")
def projects():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("projects.html", projects=data)

# dash board
@app.route("/dashboard")
def dashBoard():
    return render_template("dashboard.html")


# route for adding projects
@app.route("/addprojects", methods=["POST"])
def add_project():
    title = request.form["title"]
    description = request.form["desc"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects (title, descriptions) VALUES (%s, %s)", (title, description))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/dashboard")

# Run App
if __name__ == "__main__":
    app.run(debug=True, port=3000)
from flask import Flask, render_template, request, redirect, url_for, session, flash
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

# for showing projects (Dynamically)
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
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM admin WHERE id = %s AND name = %s"
    cursor.execute(query, (admin_id, password,))

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


# for dashboard page
@app.route("/dashboard")
def dashBoard():
    # if not logged in as admin
    if "admin_id" not in session:
        return redirect(url_for("adminLogin"))

    return render_template("dashboard.html")


# for adding projects
@app.route("/addprojects", methods=["POST"])
def add_project():
    if "admin_id" not in session:
        return redirect(url_for("adminLogin"))
    
    title = request.form["title"]
    description = request.form["desc"]
    img_link = request.form["img_link"]

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO projects (title, descriptions, image_link) VALUES (%s, %s, %s)"

    cursor.execute(query, (title, description, img_link))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Project added successfully!")

    return redirect(url_for("dashBoard"))

# for logout system
@app.route("/logout")
def log_out():
    session.clear()
    return redirect(url_for("adminLogin"))

# for getting project list
@app.route("/projectList")
def projectlist():
    if "admin_id" not in session:
        return redirect(url_for("adminLogin"))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)

    query = "SELECT title, descriptions, image_link FROM projects ORDER BY title"
    
    cursor.execute(query)
    project_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("projectList.html", projects = project_list)

# for deleting projects
@app.route("/delete_project/<string:project_title>", methods = ["POST"])
def delete_project(project_title):
    if "admin_id" not in session:
        return redirect(url_for("adminLogin"))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM projects WHERE title = %s"
    cursor.execute(query, (project_title,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Deleted Succesfully")
    return redirect(url_for("projectlist"))

# for Acheivement page
@app.route("/acheivements")
def acheivements():
    return render_template("acheivements.html")

# Run App
if __name__ == "__main__":
    app.run(debug=True, port=3000)
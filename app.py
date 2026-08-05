from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

#create flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# makes connection to database
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.execute("PRAGMA foreign_keys = on")
    conn.row_factory = sqlite3.Row

    return conn

# creates all required tables in database
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # create project table
    query = """CREATE TABLE IF NOT EXISTS projects
    (
	project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    description TEXT NOT NULL,
    
    category TEXT NOT NULL,
    thumbnail TEXT NOT NULL,
    
    challenge TEXT,
    solution TEXT,
    feature TEXT,
    future_improvement TEXT,
    
    github_link TEXT,
    demo_link TEXT,
    
    created_date DATE NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    status TEXT 
    )"""

    cursor.execute(query)

    # create technologies table
    query = """CREATE TABLE IF NOT EXISTS technologies
    (
	tech_id INTEGER PRIMARY KEY AUTOINCREMENT,
    technology TEXT UNIQUE NOT NULL
    )"""

    cursor.execute(query)

    # create projects technologies junction table
    query = """CREATE TABLE IF NOT EXISTS project_technologies
    (
	project_id INTEGER NOT NULL,
    tech_id INTEGER NOT NULL,
    
    PRIMARY KEY(project_id, tech_id),
    
    FOREIGN KEY(project_id)
		REFERENCES projects(project_id)
        ON DELETE CASCADE,
        
	FOREIGN KEY(tech_id)
		REFERENCES technologies(tech_id)
        ON DELETE CASCADE
    )"""

    cursor.execute(query)

    # temporary for testing purpose
    # create admin table
    query = """create table IF NOT EXISTS admins
    (
	admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )"""

    cursor.execute(query)

    # insert into admins
    query = "SELECT COUNT(*) FROM admins"
    cursor.execute(query)

    count = cursor.fetchone()[0]

    if count == 0:
        query = "INSERT INTO admins(username, password_hash) VALUES('ramsundar', 'ramsundar2001')"
        cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()



# ----- Home Page ----- #
@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    for p in projects:
        print(dict(p))

    cursor.execute("SELECT * FROM technologies")
    tech = cursor.fetchall()
    for t in tech:
        print(dict(t))

    cursor.execute("SELECT * FROM project_technologies")
    pt = cursor.fetchall()
    for j in pt:
        print(dict(j))


    cursor.execute("SELECT * FROM admins")
    admins = cursor.fetchall()
    for a in admins:
        print(dict(a))

    cursor.close()
    conn.close()

    return render_template("index.html")

# ----- Project Page ----- #
@app.route("/project_page")
def project_page():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT project_id, title, summary, thumbnail FROM projects"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("project.html", projects = data)

# ----- View Page ----- #
@app.route("/view/<int:project_id>")
def view_page(project_id):

    conn = None
    cursor = None
    project = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT title, summary, description, category, thumbnail, challenge, solution, feature, future_improvement, github_link, demo_link, created_date, upload_date, updated_date, status FROM projects WHERE project_id = ?"

        cursor.execute(query, (project_id,))
        project = cursor.fetchone()

    except Exception as e:
        if conn:
            conn.rollback()

        print(e)
        flash("Error While Loading Project", "view")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template("view.html", project = project)

# ----- Admin Page ----- #
@app.route("/admin_page")
def admin_page():
    return render_template("admin.html")

# ----- Admin Dashboard Page ----- #
@app.route("/dashboard", methods=["GET"])
def dashboard():
    # if not logged in as admin
    if "username" not in session:
        return redirect(url_for("admin_page"))

    return render_template("dashboard.html")

# ----- Admin Login System ----- #
@app.route("/admin_login", methods=["POST"])
def admin_login():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
    admin_id,
    username,
    password_hash,
    created_at
    FROM admins
    WHERE username = ? AND password_hash = ?
    """

    cursor.execute(query, (username, password))

    print("Entered username:", repr(username))
    print("Entered password:", repr(password))

    is_admin = cursor.fetchone()
    cursor.execute("SELECT * FROM admins")
    print(cursor.fetchall())

    cursor.close()
    conn.close()


    print ("is admin: ",is_admin)
    if is_admin:
        print ("is admin: ",is_admin)
        session["username"] = is_admin["username"]
        print("session['username']: ", session['username'])

        return redirect(url_for("dashboard"))
    
    return render_template("admin.html", error = "Invalid Id or Password")

        
# ----- Admin Logout System ----- #
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin_page"))




# ----- Add Project System ----- #
@app.route("/add_project", methods=["POST"])
def add_project():
    if "username" not in session:
        return redirect(url_for("admin_page"))
    
    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        # +--------------------------+
        # |     get form request     |
        # +--------------------------+

        # dashboard form section one data
        date = request.form["date"]
        category = request.form["category"]
        title = request.form["title"]
        summary = request.form["summary"]
        technologies = request.form.getlist("technologies")
        thumbnail = request.form["thumbnail"]
        description = request.form["description"]

        # dashboard form section two data
        challenge = request.form["challenge"]
        solution = request.form["solution"]
        feature = request.form["feature"]
        future_improvement = request.form["future_improvement"]
        status = request.form["status"]

        # +---------------------------------+
        # |     insert into the project     |
        # +---------------------------------+

        query = """INSERT INTO projects
        (
        title,
        summary,
        description,
        category,
        thumbnail,
        challenge,
        solution,
        feature,
        future_improvement,
        created_date,
        status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        cursor.execute(query, (title, summary, description, category, thumbnail, challenge, solution, feature, future_improvement, date, status,))


        # get generated project_id
        project_id = cursor.lastrowid

        # +---------------------------------------+
        # |     insert into the techonologies     |
        # +---------------------------------------+

        # insert into technologies table
        for tech in technologies:

            # check if technology exists
            cursor.execute("SELECT tech_id FROM technologies WHERE technology = ?", (tech,))

            result = cursor.fetchone()

            if result:
                tech_id = result[0]

            else:
                cursor.execute("INSERT INTO technologies(technology) values(?)", (tech,))

                tech_id = cursor.lastrowid

            # +-------------------------------+
            # |     link project and tech     |
            # +-------------------------------+

            cursor.execute("INSERT INTO project_technologies(project_id, tech_id) VALUES(?, ?)", (project_id, tech_id,))

        conn.commit()
        flash("Project Added Successfully", "project")

    except Exception as e:
        conn.rollback()

        print(e)

        flash("Error Adding Project", "project")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("dashboard"))


# ----- Update Project System ----- #
@app.route("/update_project/<int:project_id>", methods = ["GET", "POST"])
def update_project(project_id):
    if "username" not in session:
        return redirect(url_for("admin"))

    conn = None
    cursor = None
    project = None
    tech = None
    
    try:
        conn = get_db_connection()

        if request.method == "POST":
            # request dashbaord form section one data
            date = request.form["date"]
            category = request.form["category"]
            title = request.form["title"]
            summary = request.form["summary"]
            technologies = request.form.getlist("technologies")
            thumbnail = request.form["thumbnail"]
            description = request.form["description"]

            # request dashboard form section two data
            challenge = request.form["challenge"]
            solution = request.form["solution"]
            feature = request.form["feature"]
            future_improvement = request.form["future_improvement"]

            # UPDATING THE PROJECT TABLE
            query = "UPDATE projects SET created_date = ?, category = ?, title = ? , summary = ?, thumbnail = ?, description = ?, challenge = ?, solution = ?, feature = ?, future_improvement = ? WHERE project_id = ?"

            cursor = conn.cursor()
            cursor.execute(query, (date, category, title, summary, thumbnail, description, challenge, solution, feature, future_improvement, project_id,))

            # DELETING ALL ROWS FORM PROJECT_TECHNOLOGIES TABLE
            query = "DELETE FROM project_technologies WHERE project_id = ?"

            cursor.execute(query, (project_id,))

            # FRESH ENTRY IN PROJECT_TECHNOLOGIES TABLE AND ADDING NEW TECHNOLOGY TO TECHNOLOGIES TABLE
            for tech in technologies:
                query = "SELECT tech_id FROM technologies WHERE technology = ?"

                cursor.execute(query, (tech,))
                result = cursor.fetchone()

                if result:
                    tech_id = result[0]

                else:
                    query = "INSERT INTO technologies(technology) VALUES(?)"

                    cursor.execute(query, (tech,))
                    tech_id = cursor.lastrowid

                query = "INSERT INTO project_technologies (project_id, tech_id) VALUES(?, ?)"

                cursor.execute(query, (project_id, tech_id))

            conn.commit()

        else:
            cursor = conn.cursor()

            query = "SELECT project_id, created_date, category, title, summary, thumbnail, description, challenge, solution, feature, future_improvement FROM projects WHERE project_id = ?"

            cursor.execute(query, (project_id,))
            project = cursor.fetchone()

            query = "SELECT T.technology FROM technologies AS T INNER JOIN project_technologies AS PT ON PT.tech_id = T.tech_id WHERE PT.project_id = ?"

            cursor.execute(query, (project_id,))
            tech = [row["technology"] for row in cursor.fetchall()]

    except Exception as e:
            if conn:
                conn.rollback()

            print(e) # for error checking

            flash("Error While Updation", "project")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        
    if request.method == "POST":
        flash("Project Successfully Updated", "project")
        return redirect(url_for("dashboard"))
        
    return render_template("dashboard.html", mode = "edit", project = project, tech = tech)


# ----- Delete Project System ----- #
@app.route("/delete_project/<int:project_id>", methods = ["POST"])
def delete_project(project_id):
    if "username" not in session:
        return redirect(url_for("admin_page"))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM projects WHERE project_id = ?"
    cursor.execute(query, (project_id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Deleted Succesfully")
    return redirect(url_for("project_page"))

# Run App
if __name__ == "__main__":

    create_table()
    app.run(debug=True, port=3000)
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = "change_this_to_a_long_random_secret_key"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"


# Load scholarships from JSON
def load_scholarships():
    try:
        with open("scholarships.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Save scholarships to JSON
def save_scholarships(data):
    with open("scholarships.json", "w") as file:
        json.dump(data, file, indent=4)


# ===================== HOME =====================
@app.route("/")
def home():

    scholarships = load_scholarships()

    total = len(scholarships)

    countries = len(set(s["country"] for s in scholarships))

    return render_template(
        "index.html",
        scholarships=scholarships,
        total=total,
        countries=countries
    )
@app.route("/countries")
def countries():
    return render_template("countries.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

# ===================== ABOUT =====================
@app.route("/about")
def about():
    return render_template("about.html")


# ===================== VIEW SCHOLARSHIPS =====================
@app.route("/scholarships")
def scholarships():

    data = load_scholarships()

    country = request.args.get("country", "")
    field = request.args.get("field", "")
    degree = request.args.get("degree", "")
    status = request.args.get("status", "")

    if country:
        data = [
            s for s in data
            if country.lower() in s["country"].lower()
        ]

    if field:
        data = [
            s for s in data
            if field.lower() in s["field"].lower()
        ]

    if degree:
        data = [
            s for s in data
            if degree.lower() in s["degree"].lower()
        ]

    if status:
        data = [
            s for s in data
            if s["status"].lower() == status.lower()
        ]

    return render_template(
        "scholarships.html",
        scholarships=data
    )


# ===================== LOGIN =====================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin"] = True
            flash("Login successful!", "success")
            return redirect(url_for("admin"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


# ===================== ADMIN PANEL =====================
@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect(url_for("login"))

    data = load_scholarships()

    total = len(data)
    open_count = len([s for s in data if s["status"] == "Open"])
    closed_count = len([s for s in data if s["status"] == "Closed"])

    return render_template(
        "admin.html",
        total=total,
        open_count=open_count,
        closed_count=closed_count
    )


# ===================== ADD SCHOLARSHIP =====================
@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        data = load_scholarships()

        new_scholarship = {
            "name": request.form["name"],
            "country": request.form["country"],
            "field": request.form["field"],
            "degree": request.form["degree"],
            "deadline": request.form["deadline"],
            "status": request.form["status"]
}

        data.append(new_scholarship)

        save_scholarships(data)

        return redirect(url_for("scholarships"))

    return render_template("add.html")
@app.route("/delete/<int:index>")
def delete(index):

    data = load_scholarships()

    if 0 <= index < len(data):
        data.pop(index)
        save_scholarships(data)

    return redirect(url_for("scholarships"))

@app.route("/details/<int:index>")
def details(index):

    data = load_scholarships()

    if 0 <= index < len(data):
        return render_template(
            "details.html",
            scholarship=data[index]
        )

    return "Scholarship not found."

@app.route("/apply", methods=["GET", "POST"])
def apply():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        country = request.form["country"]
        reason = request.form["reason"]

        print("New Application")
        print(name)
        print(email)
        print(country)
        print(reason)

        return """
        <h1>Application Submitted Successfully!</h1>
        <a href='/'>Return Home</a>
        """

    return render_template("apply.html")
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# ===================== RUN APP =====================
if __name__ == "__main__":
    app.run(debug=True)
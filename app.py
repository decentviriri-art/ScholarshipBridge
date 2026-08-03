from flask import Flask, render_template, request, redirect, url_for, flash, session
import json

app = Flask(__name__)
app.secret_key = "ScholarshipBridge2026@SecureKey!123"

DATA_FILE = "scholarships.json"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"


# ===================== LOAD SCHOLARSHIPS =====================

def load_scholarships():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# ===================== SAVE SCHOLARSHIPS =====================

def save_scholarships(data):
    with open(DATA_FILE, "w") as file:
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


# ===================== COUNTRIES =====================

@app.route("/countries")
def countries():
    return render_template("countries.html")


# ===================== CONTACT =====================

@app.route("/contact")
def contact():
    return render_template("contact.html")


# ===================== ABOUT =====================

@app.route("/about")
def about():
    return render_template("about.html")


# ===================== SCHOLARSHIPS =====================

@app.route("/scholarships")
def scholarships():

    data = load_scholarships()

    country = request.args.get("country", "")
    field = request.args.get("field", "")
    degree = request.args.get("degree", "")
    status = request.args.get("status", "")

    if country:
        data = [s for s in data if country.lower() in s["country"].lower()]

    if field:
        data = [s for s in data if field.lower() in s["field"].lower()]

    if degree:
        data = [s for s in data if degree.lower() in s["degree"].lower()]

    if status:
        data = [s for s in data if s["status"].lower() == status.lower()]

    return render_template(
        "scholarships.html",
        scholarships=data
    )


# ===================== ADMIN LOGIN =====================

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


# ===================== ADMIN DASHBOARD =====================

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

    if not session.get("admin"):
        return redirect(url_for("login"))

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

        flash("Scholarship added successfully!", "success")

        return redirect(url_for("scholarships"))

    return render_template("add.html")
# ===================== DELETE SCHOLARSHIP =====================

@app.route("/delete/<int:index>")
def delete(index):

    if not session.get("admin"):
        return redirect(url_for("login"))

    data = load_scholarships()

    if 0 <= index < len(data):
        data.pop(index)
        save_scholarships(data)
        flash("Scholarship deleted successfully!", "success")

    return redirect(url_for("scholarships"))


# ===================== SCHOLARSHIP DETAILS =====================

@app.route("/details/<int:index>")
def details(index):

    data = load_scholarships()

    if 0 <= index < len(data):
        return render_template(
            "details.html",
            scholarship=data[index]
        )

    flash("Scholarship not found.", "danger")
    return redirect(url_for("scholarships"))


# ===================== APPLY =====================

@app.route("/apply", methods=["GET", "POST"])
def apply():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        country = request.form["country"]
        reason = request.form["reason"]

        print("New Application")
        print("Name:", name)
        print("Email:", email)
        print("Country:", country)
        print("Reason:", reason)

        flash("Application submitted successfully!", "success")

        return redirect(url_for("home"))

    return render_template("apply.html")


# ===================== STUDENT REGISTER =====================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        # Database will be added later

        print("Student Registered")
        print(fullname)
        print(email)

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("student_login"))

    return render_template("register.html")


# ===================== STUDENT LOGIN =====================

@app.route("/student-login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # Database validation will be added later

        session["student"] = email

        flash("Welcome to ScholarshipBridge!", "success")

        return redirect(url_for("student_dashboard"))

    return render_template("student_login.html")


# ===================== STUDENT DASHBOARD =====================

@app.route("/student-dashboard")
def student_dashboard():

    if "student" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("student_login"))

    return render_template(
        "student_dashboard.html",
        student=session["student"]
    )


# ===================== LOGOUT =====================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!", "success")

    return redirect(url_for("home"))


# ===================== RUN APP =====================

if __name__ == "__main__":
    app.run(debug=True)
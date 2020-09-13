
from flask import render_template, request, redirect, url_for, flash
from passlib.hash import sha256_crypt
from models import *


app = Flask(__name__)
app.secret_key = 'charitySystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2313@localhost/CharitySystem'
db.init_app(app)






@app.route('/')
def index():
    return render_template("layout0.html")


# ----------LOGIN------------#


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        myUser = User.query.filter_by(email=username).first()
        if myUser is None:
            print("NO USER")
        else:
            if sha256_crypt.verify(password, myUser.password):
                return redirect(url_for('admin'))
            else:
                print("Danger")
        print("danger")

# ----------SIGIN-IN------------#


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == "GET":
        return render_template("sign_in.html")
    else:
        fullname = request.form.get("fullname")
        address = request.form.get("address")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        secure_password = sha256_crypt.encrypt(str(password))
        register_user = User.query.filter_by(email=email).first()
        if register_user:
            if register_user.email == email:
                return redirect(url_for('sign_in'))
        else:
            if password == confirm_password:
                user = User(fullname=fullname, address=address, email=email, password=secure_password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash("Password does not match", "danger")
                return redirect(url_for('sign_in'))


@app.route('/charity_details')
def charity_details():
    return render_template("charity_details.html")


@app.route('/past_transactions')
def past_transactions():
    return render_template("past_transactions.html")


@app.route('/contact_us')
def contact_us():
    return render_template("contact_us.html")


# ----------ADMIN-PART------------#


@app.route('/admin')
def admin():
    return render_template("admin_layout.html")


@app.route('/user_details')
def user_details():
    return render_template("admin_user_details.html")


if __name__ == '__main__':
    app.run()

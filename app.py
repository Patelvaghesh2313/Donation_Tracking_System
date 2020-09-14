from flask import render_template, request, redirect, url_for, flash, g, session
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


@app.route('/dashboard')
def dashboard():
    return render_template("layout01.html",user=session['user'])


# ----------LOGIN------------#


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        session.pop('user', None)
        username = request.form.get("username")
        password = request.form.get("password")
        myUser = User.query.filter_by(email=username).first()
        if username == 'admin' and password == 'admin@123':
            session['user'] = 'admin'
            return redirect(url_for('admin'))
        else:
            if sha256_crypt.verify(password, myUser.password):
                session['user'] = username
                return redirect(url_for('dashboard'))
            return redirect(url_for('login'))
        return render_template("error.html")


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
    if g.user:
        return render_template("charity_details.html")
    return render_template("error.html")


@app.route('/past_transactions')
def past_transactions():
    if g.user:
        return render_template("past_transactions.html")
    return render_template("error.html")


@app.route('/contact_us')
def contact_us():
    if g.user:
        return render_template("contact_us.html")
    return render_template("error.html")



@app.route('/logout')
def logout():
    session.pop('user',None)
    return render_template("layout0.html")


# ----------ADMIN-PART------------#


@app.route('/admin')
def admin():
    if session['user'] == 'admin':
        return render_template("admin_layout.html", user=session['user'])
    return render_template("error.html")


@app.route('/user_details')
def user_details():
    if session['user'] == 'admin':
        return render_template("admin_user_details.html")
    return render_template("error.html")


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


if __name__ == '__main__':
    app.run()

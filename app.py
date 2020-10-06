from flask import render_template, request, redirect, url_for, flash, g, session, current_app
from passlib.hash import sha256_crypt
from models import *
from web3 import Web3
import os
import secrets

app = Flask(__name__)
app.secret_key = 'charitySystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2313@localhost/CharitySystem'
picsFolder = os.path.join('static','pics')
app.config['UPLOAD_FOLDER'] = picsFolder
db.init_app(app)


######################## HERE WE MAKE THE ROUTE OF ALL URLS#############
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", user=session['user'])


############################  LOGIN MODULE   #########################


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session.pop('user', None)
        return render_template("login.html")
    else:
        session.pop('user', None)
        username = request.form.get("username")
        password = request.form.get("password")
        myUser = User.query.filter_by(email=username).first()
        if username == 'admin' and password == 'admin@123':
            session['user'] = 'admin'
            return redirect(url_for('admin'))
        elif myUser == None:
            flash("User Does Not Exist ",'danger')
            return redirect(url_for('login'))
        else:
            if sha256_crypt.verify(password, myUser.password):
                session['user'] = username
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect Username And Password !",'danger')
                return redirect(url_for('login'))
    return render_template("error.html")
############################  END OF LOGIN MODULE  #########################

############################  SIGN-UP MODULE  #########################


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == "GET":
        session.pop('user', None)
        return render_template("sign_in.html")
    else:
        fullname = request.form.get("fullname")
        address = request.form.get("address")
        city = request.form.get("city")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        secure_password = sha256_crypt.encrypt(str(password))
        register_user = User.query.filter_by(email=email).first()
        if register_user:
            if register_user.email == email:
                return redirect(url_for('sign_in'))
        else:
            if password == confirm_password:
                user = User(fullname=fullname, address=address, city=city, email=email, phone=phone,
                            password=secure_password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash("Password does not match", 'danger')
                return redirect(url_for('sign_in'))

############################  END OF SIGN-UP MODULE #########################


@app.route('/charity_Details')
def charity_Details():
    if g.user:
        data = Charity.query.all()
        return render_template("charity_details.html",charities = data)
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
    session.pop('user', None)
    return render_template("index.html")


############################ ADMIN-PART #############################


@app.route('/admin')
def admin():
    if session['user'] == 'admin':
        return render_template("admin_dashboard.html", user=session['user'],total_users=3)
    return render_template("error.html")

############################ USER DETAILS PART #############################


@app.route('/user_details')
def user_details():
    if session['user'] == 'admin':
        all_user = User.query.all()
        return render_template("admin_user_details.html", users=all_user)
    return render_template("error.html")


@app.route('/user_details/add_user', methods=['POST'])
def add_user():
    if session['user'] == 'admin':
        fullname = request.form.get("fullname")
        address = request.form.get("address")
        city = request.form.get("city")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        secure_password = sha256_crypt.encrypt(str(password))
        register_user = User.query.filter_by(email=email).first()
        if register_user:
            if register_user.email == email:
                flash("User Already Exist", 'danger')
                return redirect(url_for('user_details'))
        else:
            if password == confirm_password:
                user = User(fullname=fullname, address=address, city=city, email=email, phone=phone,
                            password=secure_password)
                db.session.add(user)
                db.session.commit()
                flash("User Inserted Successfully",'success')
                return redirect(url_for('user_details'))
            else:
                flash("Password Does Not Match", 'danger')
                return redirect(url_for('user_details'))
    else:
        return render_template("error.html")


@app.route('/user_details/update_user', methods=['POST'])
def update_user():
    if session['user'] == 'admin':
        if request.method == 'POST':
            my_data = User.query.get(request.form.get('id'))
            my_data.fullname = request.form['fullname']
            my_data.address = request.form['address']
            my_data.city = request.form['city']
            my_data.email = request.form['email']
            my_data.phone = request.form['phone']
            updatedPassword = request.form['password']
            my_data.password = sha256_crypt.encrypt(str(updatedPassword))
            db.session.commit()
            flash("User Updated Successfully",'success')
            return redirect(url_for('user_details'))
    else:
        return render_template("error.html")


@app.route('/delete_user/<id>', methods=['GET', 'POST'])
def delete_user(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("User Deleted Successfully")
    return redirect(url_for('user_details'))
############################ END OF USER DETAILS PART #############################

#############SAVE THE IMAGE HERE WE MAKE ONE FUNCTION###################


def save_images(image):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(image.filename)
    photo_name = hash_photo + file_extension
    file_path = os.path.join(current_app.root_path, 'static/pics', photo_name)
    image.save(file_path)
    return photo_name


########################END OF SAVE IMAGE FUNCTION######################

############################ CHARITY DETAILS PART #############################

@app.route('/charity_details')
def charity_details():
    if session['user'] == 'admin':
        all_charity = Charity.query.all()
        return render_template("admin_charity_details.html",charities = all_charity)
    return render_template("error.html")


@app.route('/charity_details/add_charity', methods=['POST'])
def add_charity():
    if session['user'] == 'admin':
        title = request.form.get('title')
        content = request.form.get('content')
        image = save_images(request.files.get('image'))
        pub_date = request.form.get('pub_date')

        addCharity = Charity(title=title,content=content,image=image,pub_time=pub_date)
        db.session.add(addCharity)
        db.session.commit()
        flash("Charity Added Successfully",'success')
        return redirect(url_for('charity_details'))
    return render_template("error.html")


@app.route('/delete_charity/<id>', methods=['GET', 'POST'])
def delete_charity(id):
    my_data = Charity.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Charity Deleted Successfully",'success')
    return redirect(url_for('charity_details'))

############################ END OF CHARITY DETAILS PART #############################


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

#################### END OF ADMIN PART ########################


if __name__ == '__main__':
    app.run()

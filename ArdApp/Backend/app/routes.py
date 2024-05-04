from flask import Blueprint, render_template, redirect, url_for, request, flash, g
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_, and_

from models import User, History
from app import db

main = Blueprint('main', __name__)

@main.route('/register', methods = ["POST", "GET"])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('main.login_page'))

    return render_template('register.html')

@main.route('/login', methods = ['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')
            
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.main_page'))
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('login.html')

@main.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.register'))

@main.route('/add', methods=['POST'])
def add_data():
    login = request.json['login']
    password = request.json['password']
    if login and password:
        user = User.query.filter_by(login=login).first()
        
        if user and check_password_hash(user.password, password):
            index = user.id
            st = request.json['soil_temperature']
            sh = request.json['soil_humidity']
            at = request.json['air_temperature']
            ah = request.json['air_humidity']
            li = request.json['light_intensity']
            entry = History(user_id=index, soil_temperature = st, soil_humidity = sh, air_temperature = at, air_humidity = ah, light_intensity = li)
            db.session.add(entry)
            db.session.commit()

            last_entry= History.query.filter_by(user_id=index).order_by(History.id.desc()).first()
            st = last_entry.soil_temperature
            sh = last_entry.soil_humidity
            at = last_entry.air_temperature
            ah = last_entry.air_humidity
            li = last_entry.light_intensity

        return {}
        

@main.route('/', methods = ['GET'])
@login_required
def main_page():
    index = current_user.get_id()
    last_entries= History.query.filter_by(user_id=index).order_by(History.id.desc()).limit(10)
    data_date = []
    data_st = []
    data_sh = []
    data_at = []
    data_ah = []
    data_li = []
    
    for entry in last_entries:
        print(entry)
        data_date.append(entry.id)
        data_st.append(entry.soil_temperature)
        data_sh.append(entry.soil_humidity)
        data_at.append(entry.air_temperature)
        data_ah.append(entry.air_humidity)
        data_li.append(entry.light_intensity)

    labels = list(reversed(data_date))
    values = list(reversed(data_st))
 
    # Return the components to the HTML template 
    return render_template("chart.html", labels=labels, data_st=data_st, data_sh=data_sh, data_at=data_at, data_ah=data_ah, data_li=data_li)

@main.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('main.login_page') + '?next=' + request.url)

    return response
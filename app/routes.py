import os
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, bcrypt
from app.forms import TherapistLoginForm, TherapistRegistrationForm, PatientSignUpForm, TreatmentSignUpForm
from app.models import Patient, User, Treatment

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/account')
@login_required
def account():
    patients = Patient.query.all()
    return render_template('account.html', title='Account', patients=patients)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = TherapistRegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = TherapistLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
@login_required
def signup():
    form = PatientSignUpForm()
    if form.validate_on_submit():
        patient = Patient(firstname=form.firstname.data, lastname=form.lastname.data, dateofbirth=form.dateofbirth.data,
                                                                                     therapist=current_user)
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('treatmentsignup'))
    return render_template('signup.html', title='Sign Up Patients', form=form)

@app.route('/treatmentsignup', methods=['GET', 'POST'])
@login_required
def treatmentsignup():
    form = TreatmentSignUpForm()
    if form.validate_on_submit():
        treatment = Treatment(treatmentname=form.treatmentname.data, treatmentnotes=form.treatmentnotes.data,
                                        treatmentdate=form.treatmentdate.data, treatmentprice=form.treatmentprice.data,
                                        patientref=current_user)
        db.session.add(treatment)
        db.session.commit()
        flash('You have added a patient successfully')
        return redirect(url_for('account'))
    return render_template('treatmentsignup.html', title='Sign Up Patients', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

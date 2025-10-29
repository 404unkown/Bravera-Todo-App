from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from web.models import User, db, Note
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password1):
            login_user(user, remember=True)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password.', category='error')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(username) < 2:
            flash('Username should be greater than 2 characters.', category='error')
        elif len(email) < 2:
            flash('Email should be greater than 2 characters.', category='error')
        elif len(password1) < 7:
            flash('Password should be greater than 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists!', category='error')
            else:
                new_user = User(username=username, email=email)
                new_user.set_password(password1)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created successfully!', category='success')
                return redirect(url_for('views.home'))
    return render_template('register.html')

@auth.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')
        if len(title) < 1:
            flash('Title must be greater than 1 character.', category='error')
        elif len(note) < 2:
            flash('The journal must be greater than 2 characters.', category='error')
        else:
            new_note = Note(title=title, note=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Journal added successfully.', category='success')
    return render_template('journal.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return jsonify({})

@auth.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    note = Note.query.get_or_404(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.note = request.form['note']
        db.session.commit()
        flash('Updated successfully!', category='success')
        return redirect(url_for('auth.journal'))
    return render_template('update_note.html', note=note)

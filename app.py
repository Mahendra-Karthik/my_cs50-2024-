from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import pandas as pd
import os
from config import db, Config
from forms import LoginForm, AddQuestionForm, RegistrationForm 
from models import User, Question, ExamResult
from helpers import grade_exam  # Keeping the grading logic in helpers

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Set the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit to 16 MB

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))  # Redirect to the login page


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.is_examiner.data and form.secret_password.data != 'examiner@123':
            flash('Creation failed: Invalid secret password.', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=form.username.data, is_examiner=form.is_examiner.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')  # Add 'danger' category for Bootstrap styling
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_examiner:  # Check if the user is an examiner
        return render_template('admin_dashboard.html')  # Admin dashboard
    return render_template('dashboard.html')  # Regular user dashboard

# Generate exam questions from the database
def generate_exam():
    questions = Question.query.all()  # Fetch all questions from the database
    return questions

@app.route('/exam', methods=['GET', 'POST'])
@login_required
def exam():
    if request.method == 'POST':
        answers = request.form
        score = grade_exam(answers)  # Grade the exam using the helper function
        result = ExamResult(user_id=current_user.id, score=score)
        db.session.add(result)
        db.session.commit()
        return redirect(url_for('view_results'))

    questions = generate_exam()  # Fetch exam questions
    return render_template('exam.html', questions=questions)

@app.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    form = AddQuestionForm()
    if form.validate_on_submit():
        question = Question(
            content=form.content.data,
            option1=form.option1.data,
            option2=form.option2.data,
            option3=form.option3.data,
            option4=form.option4.data,
            answer=form.answer.data
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully')
        return redirect(url_for('dashboard'))
    return render_template('add_question.html', form=form)

@app.route('/view_results')
@login_required
def view_results():
    result = ExamResult.query.filter_by(user_id=current_user.id).order_by(ExamResult.id.desc()).first()
    return render_template('view_results.html', result=result)


@app.route('/admin/view_results')
@login_required
def admin_view_results():
    if not current_user.is_examiner:
        return redirect(url_for('dashboard'))  # Redirect if not an admin

    # Fetch the latest result for each user
    latest_results = db.session.query(ExamResult).distinct(ExamResult.user_id).order_by(ExamResult.user_id, ExamResult.id.desc()).all()

    return render_template('admin_view_results.html', results=latest_results)

@app.route('/admin/upload_questions', methods=['GET', 'POST'])
@login_required
def upload_questions():
    if not current_user.is_examiner:
        return redirect(url_for('dashboard'))  # Redirect if not an admin

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Questions uploaded successfully')
            return redirect(url_for('admin_view_results'))
        else:
            flash('Invalid file format. Please upload a CSV file.', 'danger')

    return render_template('upload_questions.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

def process_csv(filepath):
    # Read CSV file
    df = pd.read_csv(filepath)
    for index, row in df.iterrows():
        question = Question(
            content=row['content'],
            option1=row['option1'],
            option2=row['option2'],
            option3=row['option3'],
            option4=row['option4'],
            answer=row['answer']
        )
        db.session.add(question)
    db.session.commit()

# Command to create a new user from the CLI
@app.cli.command('create_user')
def create_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    is_examiner_input = input("Is this user an examiner/admin? (y/n): ").lower() == 'y'
    new_user = User(username=username, is_examiner=is_examiner_input)  # Set examiner flag
    new_user.set_password(password)  # Hash the password
    db.session.add(new_user)
    db.session.commit()
    print(f"User {username} created as {'Examiner' if is_examiner_input else 'Regular User'}.")

# Route to create the database
@app.route('/create_db')
def create_db():
    db.create_all()  # This will create the tables in the database
    return "Database created!"

if __name__ == '__main__':
    app.run(debug=True)

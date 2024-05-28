from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Todo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SECRET_KEY'] = 'supersecretkey'
bcrypt = Bcrypt(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('todos'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/todos', methods=['GET', 'POST'])
def todos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        todo_text = request.form['todo']
        new_todo = Todo(text=todo_text, user_id=session['user_id'])
        db.session.add(new_todo)
        db.session.commit()
    todos = Todo.query.filter_by(user_id=session['user_id']).all()
    return render_template('todos.html', todos=todos)

if __name__ == '__main__':
    app.run(debug=True)

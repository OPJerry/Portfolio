from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Projekt w fazie Alpha testów

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SECRET_KEY'] = 'supersekretnyklucz'

db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    last_order = db.Column(db.String(200), default='')

@app.route('/')
def index():
    clients = Client.query.all()
    return render_template('index.html', clients=clients)

@app.route('/add', methods=['POST'])
def add_client():
    name = request.form.get('name')
    new_client = Client(name=name)
    db.session.add(new_client)
    db.session.commit()
    flash('Klient został dodany!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

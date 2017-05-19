from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/python-attempt-4'
app.debug = True
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return '<Person %r>' % self.name

## GET ALL, <HAS POST FORM>
@app.route('/')
def index():
    myPerson = Person.query.all()
    return render_template('add_person.html', myPerson=myPerson)

## EDIT PAGE
@app.route('/profile/edit/<id>')
def update_person(id):
    person = Person.query.filter_by(id=id).first()
    return render_template('edit.html', person=person)

## EDIT POST/UPDATE ROUTE <EDIT FORM SUBMIT DESTINATION>
@app.route('/profile/edit/<id>/update', methods=['POST'])
def edit_person(id):
    formData = Person(request.form['name'], request.form['age'])
    person = Person.query.filter_by(id=id).first()
    person.name = formData.name
    person.age = formData.age
    db.session.commit()
    return redirect('/')

## DELETE ROUTE
@app.route('/profile/delete/<id>', methods=['POST'])
def delete_person(id):
    person = Person.query.filter_by(id=id).first()
    db.session.delete(person)
    db.session.commit()
    return redirect('/')

## VIEW ID PAGE
@app.route('/profile/<id>')
def profile(id):
    person = Person.query.filter_by(id=id).first()
    return render_template('profile.html', person=person)

@app.route('/post-person', methods=['POST'])
def post_person():
    person = Person(request.form['name'], request.form['age'])
    db.session.add(person)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run()

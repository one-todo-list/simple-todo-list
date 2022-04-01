from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean)

#db.create_all()

@app.route('/update/<int:todo_id>', methods=["POST", "GET"])
def edit(todo_id):
    item = Todo.query.filter_by(id=todo_id).first()
    item.completed = not item.completed
    db.session.commit()
    redirect(url_for("list_items"))


@app.route('/', methods=["GET"])
def list_items():
    todo_list = Todo.query.all()
    return render_template('list.html', todo_list=todo_list)

#Add an item
@app.route('/add', methods=['GET', 'POST'])
def add():
    title = request.form.get("title")
    item = Todo(title=title, completed=False)
    db.session.add(item)
    db.session.commit()
    redirect(url_for("list_items"))
    return render_template('list.html')

@app.route('/delete:<int:todo_id>', methods=['GET', 'POST'])
def delete(todo_id):
    item = Todo.query.filter_by(id=todo_id)
    db.session.delete(item)
    db.session.commit()
    redirect(url_for("list_items"))





if __name__ == "__main__":
    app.run(debug=True)


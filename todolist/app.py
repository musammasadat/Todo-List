

from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/new06/OneDrive/Desktop/todolist/user.db'
app.config["SECRET_KEY"] = "your_secret_key"

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)



@app.route("/")
def index():
    todos = Todo.query.all() #bir tabloda depolanan tüm kayıtları sorgulayıp bir liste olarak döndürmek için kullanılır.
    return render_template("index.html",todos = todos)


@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    """if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True"""
    todo.complete = not todo.complete

    db.session.commit()
 #Flask'teki session özelliği, kullanıcının tarayıcısındaki geçici verileri saklamak için kullanılan bir yapıdır.
    return redirect(url_for("index"))


@app.route("/add",methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title,complete = False)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))



@app.route("/todolistem")
def todolist():
    todos = Todo.query.all()
    return render_template("todolistem.html", todos = todos)


if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        print("Veritabani oluşturuldu.")
    app.run(debug=True)

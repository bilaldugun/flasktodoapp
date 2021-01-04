from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/bdugu/Desktop/Uygulama/Udemy-Python Kursu/Flask-Framework/ToDoApp/todo.db' # bu üs satır her zaman alınır.
db = SQLAlchemy(app)


@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos = todos)

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()# id si 1 olan değeri alır ve todo objesi oluşr.
    todo.complete = not(todo.complete)

    db.session.commit()#database e verileri işle
    return redirect(url_for("index"))
    



@app.route("/add" ,methods= ["POST"] ) # index.html de 16.satırdaki kodda " action = /app" olduğu için isimi bu şekilde verdik. 
def appTodo():
    title = request.form.get("title")# title nameine sahip değeri burada alıyoruz.
    newTodo = Todo(title = title, complete = False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


class Todo(db.Model): # bu sınıf ile veri tabanına kayıt edilecek veriler eklendi
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)


if __name__ == "__main__":
    db.create_all()#tablo oluşturuldu
    app.run(debug=True)
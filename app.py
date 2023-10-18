from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}"

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")

@app.route('/Modify/<int:sno>', methods=['GET', 'POST'])
def Modify(sno):
    allTodo = Todo.query.filter_by(sno=sno).first()

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        allTodo.title = title
        allTodo.desc = desc
        db.session.commit()
        return redirect("/")
    
    return render_template('Modify.html', allTodo=allTodo)

     
    # return render_template('Modify.html',allTodo=allTodo)
    


if __name__ == "__main__":
    app.run(debug=True, port=8000)

from flask import Flask, request, jsonify,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
# Or for MySQL: 'mysql://username:password@localhost/db_name'
# Or for PostgreSQL: 'postgresql://username:password@localhost/db_name'
class Todo(db.Model):  # ✅ Remove the parentheses here
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/create')
def create():
    db.create_all()
    return "Database and tables created!"

@app.route('/',methods=['GET','POST'])
def hello_world():
    # return 'hello_world'
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('hello_world'))
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.get(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    todo=Todo.query.get(sno)
    if request.method=='POST':
         todo.title=request.form['title']
         todo.desc=request.form['desc']
         db.session.commit()
         return redirect('/')
    return render_template('update.html', todo=todo)
        
@app.route('/about')
def about():
    return render_template("about.html")        


@app.route('/show')
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return "This is products page"

if __name__=="__main__":
    app.run(debug=True,port=8000)
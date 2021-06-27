from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#Flask object is the app
app=Flask(__name__)

#adding database and specifying it as sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#initialize the database for our app
db=SQLAlchemy(app) 

#this class will create a model for each entry to the app, add in columns whch are single datapoints
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #return the task and id of the task that has been created
    def __repr__(self):
        return '<Task %r>' %self.id

#routing urls using decorator 'app.route'
# the if-selse block checks if entry is null and prevents adding it to db
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        if task_content == '':
            return redirect('/')
        else:
            new_task  = Todo(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except: 
                return 'Error pushing to DB'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

# when the delete url is called it sends the post id as GET which is deleted from the DB using an ORM query
# after deletion user is redirected to the base url
@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Todo.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except: 
        return 'Error deleting entry'

# when clicked on update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except: 
            return 'Error updating entry'
    else:
        return render_template('update.html', task=task)


#usual 'int is main' function
if __name__=="__main__":
    app.run(debug=True)
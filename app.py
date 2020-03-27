from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Integer, default=0)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return f'<Todo {self.id}'

db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
  if (request.method == 'POST'):
    todo_content = request.form['content']
    if (len(todo_content) > 0):
      new_todo = Todo(content=todo_content)
      try:
        db.session.add(new_todo)
        db.session.commit()
      except:
        # TODO: Add err page
        pass
    return redirect('/')
  else:
    todos = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.jinja', todos=todos)

@app.route('/delete/<int:id>')
def delete(id):
  todo = Todo.query.get_or_404(id)
  try:
    db.session.delete(todo)
    db.session.commit()
  except:
    # TODO: Add err page
    pass
  return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  todo = Todo.query.get_or_404(id)
  if (request.method == 'POST'):
    todo.content = request.form['content']
    try:
      db.session.commit()
    except:
      # TODO: Add err page
      pass
    return redirect('/')
  else:
    return render_template('update.jinja', todo=todo)

if __name__ == "__main__":
  app.run(debug=True)
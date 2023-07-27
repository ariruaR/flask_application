from flask import Flask, render_template, request, url_for, redirect
from flask_restful import Resource,Api
from rocket import Rocket
from forms import RegisterForm, LoginForm
import sqlite3
app = Flask(__name__)
api = Api()
app.config['SECRET_KEY'] = 'Hvfjhbkjrh3742675yhhgwhb'

db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()
db.execute("""CREATE TABLE IF NOT EXISTS users(
      username TEXT,
      password TEXT,
      balance BIGINT
    )""")
db.commit()

class User:
  def __init__(self,username,password):
    self.username = username
    self.password = password
    db.execute(f"INSERT INTO users (username, password, balance) VALUES (?,?,?);", (f"{self.username}", f"{self.password}", 0))
    db.commit()


def get_deposite(username, deposite):
  db.execute("UPDATE users SET balance = balance + ? WHERE username = ?", (deposite, username))
  db.commit()


@app.route('/')
def main():
  username = request.args.get('username')
  user_info = db.execute(f'SELECT * FROM users WHERE username = "{username}"').fetchall()
  return render_template('main.html', username=username)


@app.route('/play/rocket')
def play_rocket():
  query = request.args.get('bid')
  username = request.args.get('username')
  if username == None or username == '':
    return render_template('error_page.html', error='Неизвестный пользователь')
  if query and query != '':
    balance = db.execute(f'SELECT balance FROM users WHERE username = "{username}"').fetchall()
    db.execute(f"UPDATE users SET balance = balance - ? WHERE username = '{username}'", (int(query)))
    rocket = Rocket(query)
    return render_template('rocket.html', text=f'{rocket.play()}', text2=f'Ваш выигрыш: {rocket.get_bid()}', username=username, text3=balance[0])
  else:
    return render_template('rocket.html', text='Вы не указали ставку') 

@app.route('/signup',methods=['GET', 'POST'])
def sign_up():

  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    resp = db.execute(f"SELECT * FROM users WHERE username = '{username}'").fetchall()
  # проверка и создание юзера
    if len(resp) == 0: 
      user = User(username, password)
      return redirect(url_for('login'))
    return render_template('error_page.html', error='Пользователь с этим именем уже существует')
  return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    resp = db.execute(f"SELECT password FROM users WHERE username = '{username}'").fetchall()
    if password != resp[0][0]:
      return render_template('error_page.html', text='Password Error', error='Неверные логин или пароль')
    return redirect(url_for('.userprofile', username=username))
  return render_template('login.html') 


@app.route('/user/<string:username>')
def userprofile(username):
  user = cursor.execute(f"SELECT * FROM users WHERE username = '{username}'").fetchall()
  return render_template('userprofile.html', username=user[0][0], user=user)


@app.route('/pay/deposite', methods=['GET', 'POST'])
def deposite():
  if request.method == 'POST':
    username = request.args.get('username')
    deposite = request.form.get('deposite')
    resp = db.execute(f"SELECT * FROM users WHERE username = '{username}'").fetchall()
    if len(resp) != 0:
      get_deposite(username, deposite)
      return redirect(url_for('userprofile', username=username))
  return render_template('paypage.html')

# API REALISATION
class Main(Resource):
  def get(self): ...

# api.add_resource(Main, 'v1/apiMain')
# api.init_app(app)

if __name__ == "__main__":
  app.run(debug=True)
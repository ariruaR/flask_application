from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from flask_restful import Resource,Api
from rocket import Rocket
from forms import RegisterForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
api = Api()
app.config['SECRET_KEY'] = 'Hvfjhbkjrh3742675yhhgwhb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(id):
  return db.session.query(Users).get(id)



class Users(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(500), nullable=True)
  balance = db.Column(db.Integer, default=0)
  
  def __repr__(self):
    return f"<username {self.username}>"
  
  def check_password(self, password_hash, password):
    return check_password_hash(password_hash, password)

def get_deposite(username, deposite):
  user = db.session.query(Users).filter(Users.username==username).first()
  user.balance += int(deposite)
  db.session.flush()
  db.session.commit()









@app.route('/')
def main():
  if current_user.is_authenticated == False:
    flash('Sign Up Please')
  return render_template('main.html')


@app.route('/play/rocket')
@login_required
def play_rocket():
  username = current_user.username
  bid = request.args.get('bid')
  try:
    if bid != None:
      if current_user.balance >= int(bid):
        rocket = Rocket(bid)
        result_coef = rocket.play()
        current_user.balance += rocket.get_bid() - float(bid) 
        db.session.flush()
        db.session.commit()
        return render_template('rocket.html',
        username=username,
        text=result_coef,
          text2=rocket.get_bid(),
          text3=int(current_user.balance),
          text4=bid
          )       
      if current_user.balance < int(bid):
        flash('Недостаточно средств')
        return redirect(url_for('.deposite'))
      return render_template('rocket.html',
      username=username,
      text3=int(current_user.balance),
      text4=bid)
    return render_template('rocket.html', username=username, text3=int(current_user.balance))
  except ValueError:
    flash('Invalid bid')
    return redirect('rocket')

@app.route('/signup',methods=['GET', 'POST'])
def sign_up():

  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    u = Users(username=username, password=generate_password_hash(password))
    db.session.add(u)
    db.session.flush()
    db.session.commit()
    return redirect(url_for('login'))
  return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    password_hash = db.session.query(Users).filter(Users.username == username).first()
    user = db.session.query(Users).filter(Users.username == username).first()
    if user and user.check_password(password_hash.password, password):
      remember = request.form.get('remember-me-checkbox')
      login_user(user, remember=remember)
      return redirect(url_for('.userprofile'))
    flash("Invalid username/password", 'error')
  return render_template('login.html') 


@app.route('/userprofile')
def userprofile():
  return render_template('userprofile.html', username=current_user.username)


@app.route('/pay/deposite', methods=['GET', 'POST'])
def deposite():
  if request.method == 'POST':
    username = current_user.username
    deposite = request.form.get('deposite')
    resp = Users.query.filter_by(username=username).all()
    if len(resp) != 0:
      get_deposite(username, deposite)
      return redirect(url_for('userprofile', username=username))
  return render_template('paypage.html')
@app.route('/userprofile/logout')
@login_required
def logout():
  logout_user()
  flash('Вы успешно вышли с аккаунта')
  return redirect(url_for('login'))



# API REALISATION
class Main(Resource):
  def get(self): ...

# api.add_resource(Main, 'v1/apiMain')
# api.init_app(app)
with app.app_context():
  db.create_all()

if __name__ == "__main__":
  app.run(host='127.0.0.1',port=2000,debug=True)

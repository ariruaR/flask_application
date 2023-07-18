from flask import Flask, render_template, request, url_for
from flask_restful import Resource,Api
from rocket import Rocket
from forms import RegisterForm, LoginForm

app = Flask(__name__)
api = Api()
app.config['SECRET_KEY'] = 'Hvfjhbkjrh3742675yhhgwhb'



@app.route('/')
def main():
  return render_template('main.html')
@app.route('/play/rocket')
def play_rocket():
  query = request.args.get('bid')
  if query and query != '':
    rocket = Rocket(query)
    return render_template('rocket.html', text=f'{rocket.play()}', text2=f'Ваш выигрыш: {rocket.get_bid()}')
  else:
    return render_template('rocket.html', text='Вы не указали ставку') 

@app.route('/signup',methods=['GET', 'POST'])
def sign_up():
  form = RegisterForm()
  return render_template('signup.html', form=form)
@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  return ...



# API REALISATION
class Main(Resource):
  def get(self): ...

# api.add_resource(Main, 'v1/apiMain')
# api.init_app(app)

if __name__ == "__main__":
  app.run(debug=True)
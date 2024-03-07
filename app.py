from flask import Flask, render_template, request
from flask_restful import Api
from database import db
from resources import routes

app = Flask(__name__, static_folder='static')
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost:27017/StitchXcel'
}

# Set your SECRET_KEY and JWT_SECRET_KEY here (replace 'your_secret_key' and 'your_jwt_secret_key')
app.config['SECRET_KEY'] = '1234asdf#$%&hjkl'


api = Api(app)

# initialize db
db.initialize_db(app)
# initialize routes
routes.initialize_routes(api)

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/login')
def login():
      return render_template('Login-Signup.html')
@app.route("/blog")
def blog():
      return render_template('Blogs.html')
@app.route('/about')
def about():
        return render_template('About Us.html')
@app.route('/tailor')
def tailor():
        return render_template('tailors.html')

@app.route('/tailor_profile')
def tailor_prof():
      return render_template('tailor_profile.html')

@app.route('/customer_profile')
def customer_prof():
      return render_template('customer_profile.html')

@app.route('/customer_dashboard')
def customer_dash():
      return render_template('Customer_dashboard.html')

@app.route('/tailor_dashboard')
def tailor_dash():
      return render_template('Tailor_dashboard.html')

@app.route('/post_order')
def post_order():
      return render_template('placeorder.html')
@app.route('/edit_customer')
def edit_customer():
      return render_template('edit_customer.html')



if __name__ == '__main__':
    app.run(debug=True, port=8001)

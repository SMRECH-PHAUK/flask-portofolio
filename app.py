import os
from flask import Flask, render_template
from database import db
from models import *
from university import university_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register blueprints
app.register_blueprint(university_bp, url_prefix='/university')

# Portfolio routes
@app.route('/')
def portfolio():
    return render_template('portfolio.html')

@app.route('/project2')
def project2():
    return render_template('project2.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
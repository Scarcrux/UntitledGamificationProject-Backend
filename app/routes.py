from app import app
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/index')
def index():
    return "Get off my lawn! If you're looking for the frontend, click here."

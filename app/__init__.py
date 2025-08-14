from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import json
import os
# Extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = 'routes.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY',
    '4810f5b06aae3d7b426d1537e6366e48'
)

    db_url = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .models import User  # 🔑 Needed for login manager
    from .routes import bp as routes
    app.register_blueprint(routes)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # 🔥 This solves the error

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403
    
    # Register custom Jinja filter
    @app.template_filter('from_json')
    def from_json_filter(s):
        try:
            return json.loads(s)
        except (TypeError, json.JSONDecodeError):
            return {}

    return app

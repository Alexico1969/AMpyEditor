from flask import Flask, redirect, url_for
from auth import auth_blueprint, init_oauth
from editor import editor_blueprint
from flask_login import LoginManager, current_user
from user import User

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize OAuth
init_oauth(app)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(editor_blueprint, url_prefix="/editor")

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('editor.editor'))
    return redirect(url_for('auth.login'))



if __name__ == '__main__':
    app.run(debug=True)

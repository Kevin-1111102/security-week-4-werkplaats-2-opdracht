from flask import Flask

from controllers.login import login_routes
from controllers.prompt import prompt_routes
from controllers.question import question_routes
from controllers.user import user_routes

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key

app.register_blueprint(login_routes)
app.register_blueprint(user_routes)
app.register_blueprint(question_routes)
app.register_blueprint(prompt_routes)

if __name__ == "__main__":
    app.run(debug=True)

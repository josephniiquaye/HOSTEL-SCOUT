from flask import Flask, render_template
from config import Config
from extensions import db, migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

# Import models after initializing db
from models.user import User


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
from datetime import date

from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Saying, Theme

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wisdom.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/themes")
def get_themes():
    themes = Theme.query.order_by(Theme.name).all()
    return jsonify([theme.to_dict() for theme in themes])


@app.route("/api/sayings")
def get_sayings():
    theme = request.args.get("theme")
    search = request.args.get("q")

    query = Saying.query

    if theme:
        query = query.join(Saying.themes).filter(Theme.name == theme)

    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                Saying.text.ilike(like),
                Saying.author.ilike(like),
                Saying.source.ilike(like),
                Saying.themes.any(Theme.name.ilike(like)),
            )
        )

    sayings = query.order_by(Saying.id).all()
    return jsonify([saying.to_dict() for saying in sayings])


@app.route("/api/sayings/daily")
def daily_saying():
    sayings = Saying.query.order_by(Saying.id).all()
    if not sayings:
        return jsonify({"error": "No sayings yet"}), 404

    # Same saying all day: the index comes from today's date
    index = date.today().toordinal() % len(sayings)
    return jsonify(sayings[index].to_dict())


if __name__ == "__main__":
    app.run(debug=True)
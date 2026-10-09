from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Link table: one saying can have many themes, one theme can have many sayings
saying_themes = db.Table(
    "saying_themes",
    db.Column("saying_id", db.Integer, db.ForeignKey("sayings.id"), primary_key=True),
    db.Column("theme_id", db.Integer, db.ForeignKey("themes.id"), primary_key=True),
)


class Saying(db.Model):
    __tablename__ = "sayings"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(120))
    source = db.Column(db.String(200))
    tradition = db.Column(db.String(80))
    reflection = db.Column(db.Text)

    themes = db.relationship("Theme", secondary=saying_themes, back_populates="sayings")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "author": self.author,
            "source": self.source,
            "tradition": self.tradition,
            "reflection": self.reflection,
            "themes": [theme.name for theme in self.themes],
        }


class Theme(db.Model):
    __tablename__ = "themes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    sayings = db.relationship("Saying", secondary=saying_themes, back_populates="themes")

    def to_dict(self):
        return {"id": self.id, "name": self.name}
from app import app
from models import db, Saying, Theme

SEED = [
    {
        "text": "Trust in the LORD with all thine heart; and lean not unto thine own understanding.",
        "author": "Solomon",
        "source": "Proverbs 3:5 (KJV)",
        "tradition": "Bible",
        "themes": ["faith", "wisdom"],
    },
    {
        "text": "A soft answer turneth away wrath: but grievous words stir up anger.",
        "author": "Solomon",
        "source": "Proverbs 15:1 (KJV)",
        "tradition": "Bible",
        "themes": ["relationships", "patience"],
    },
    {
        "text": "Pride goeth before destruction, and an haughty spirit before a fall.",
        "author": "Solomon",
        "source": "Proverbs 16:18 (KJV)",
        "tradition": "Bible",
        "themes": ["humility"],
    },
    {
        "text": "Wisdom is the principal thing; therefore get wisdom: and with all thy getting get understanding.",
        "author": "Solomon",
        "source": "Proverbs 4:7 (KJV)",
        "tradition": "Bible",
        "themes": ["wisdom", "purpose"],
    },
    {
        "text": "A merry heart doeth good like a medicine: but a broken spirit drieth the bones.",
        "author": "Solomon",
        "source": "Proverbs 17:22 (KJV)",
        "tradition": "Bible",
        "themes": ["joy", "health"],
    },
    {
        "text": "The unexamined life is not worth living.",
        "author": "Socrates",
        "source": "Plato, Apology 38a",
        "tradition": "Greek philosophy",
        "themes": ["wisdom", "purpose"],
    },
    {
        "text": "Such as are thy habitual thoughts, such also will be the character of thy mind; for the soul is dyed by the thoughts.",
        "author": "Marcus Aurelius",
        "source": "Meditations 5.16 (George Long translation)",
        "tradition": "Stoic",
        "themes": ["mindset", "wisdom"],
    },
    {
        "text": "A journey of a thousand miles begins with a single step.",
        "author": "Lao Tzu",
        "source": "Tao Te Ching, chapter 64",
        "tradition": "Taoist",
        "themes": ["patience", "purpose"],
    },
]


def get_or_create_theme(name):
    theme = Theme.query.filter_by(name=name).first()
    if not theme:
        theme = Theme(name=name)
        db.session.add(theme)
    return theme


with app.app_context():
    added = 0
    for item in SEED:
        if Saying.query.filter_by(text=item["text"]).first():
            continue  # skip duplicates so the script is safe to re-run
        saying = Saying(
            text=item["text"],
            author=item["author"],
            source=item["source"],
            tradition=item["tradition"],
        )
        saying.themes = [get_or_create_theme(name) for name in item["themes"]]
        db.session.add(saying)
        added += 1
    db.session.commit()
    print(f"Added {added} sayings. Total now: {Saying.query.count()}")
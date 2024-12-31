from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Iris(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sepal_length = db.Column(db.Float, nullable=False)
    sepal_width = db.Column(db.Float, nullable=False)
    petal_length = db.Column(db.Float, nullable=False)
    petal_width = db.Column(db.Float, nullable=False)
    category = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "sepal_length": self.sepal_length,
            "sepal_width": self.sepal_width,
            "petal_length": self.petal_length,
            "petal_width": self.petal_width,
            "category": self.category
        }

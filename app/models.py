from dataclasses import dataclass
from . import db


@dataclass
class Product(db.Model):  # type: ignore[misc]
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(120), nullable=False, index=True)
    category: str = db.Column(db.String(80), nullable=True, index=True)
    available: bool = db.Column(db.Boolean, default=True, nullable=False, index=True)
    price: float = db.Column(db.Float, default=0.0, nullable=False)
    description: str = db.Column(db.String(255), default="", nullable=False)

    def update_from_dict(self, data: dict) -> None:
        for field in ["name", "category", "available", "price", "description"]:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "available": self.available,
            "price": self.price,
            "description": self.description,
        }

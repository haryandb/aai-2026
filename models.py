from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True)
    invoice_no = db.Column(db.String(20))
    stock_code = db.Column(db.String(20))
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    invoice_date = db.Column(db.DateTime)
    unit_price = db.Column(db.Float)
    customer_id = db.Column(db.Float)
    country = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "invoice_no": self.invoice_no,
            "stock_code": self.stock_code,
            "description": self.description,
            "quantity": self.quantity,
            "invoice_date": self.invoice_date.isoformat()
            if self.invoice_date
            else None,
            "unit_price": self.unit_price,
            "customer_id": self.customer_id,
            "country": self.country,
        }

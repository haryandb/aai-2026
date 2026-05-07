import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_migrate import Migrate
from sqlalchemy import func
import pickle

from models import db, User, Transaction
from seeds import register_commands

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

register_commands(app, db)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_item_based.pkl")
model_data = None
try:
    with open(MODEL_PATH, "rb") as f:
        model_data = pickle.load(f)
    print(f"Model loaded: {len(model_data['item_list'])} items")
except Exception as e:
    print(f"Warning: Could not load model: {e}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products")
def products():
    page = request.args.get("page", 1, type=int)
    per_page = 12
    search = request.args.get("q", "", type=str)

    query = db.session.query(
        Transaction.stock_code,
        func.max(Transaction.description).label("description"),
        func.max(Transaction.unit_price).label("unit_price"),
    ).group_by(Transaction.stock_code)

    if search:
        query = query.filter(Transaction.description.ilike(f"%{search}%"))

    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return jsonify(
        {
            "products": [
                {
                    "stock_code": p.stock_code,
                    "description": p.description,
                    "unit_price": p.unit_price,
                    "image_url": f"https://picsum.photos/seed/{p.stock_code}/300/300",
                }
                for p in items
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
        }
    )


@app.route("/products/<stock_code>")
def product_detail(stock_code):
    product = (
        db.session.query(
            Transaction.stock_code,
            func.max(Transaction.description).label("description"),
            func.max(Transaction.unit_price).label("unit_price"),
        )
        .filter(Transaction.stock_code == stock_code)
        .group_by(Transaction.stock_code)
        .first()
    )

    if not product:
        return "Product not found", 404

    rec_descriptions = []
    if model_data and product.description in model_data["similarity_matrix"].index:
        sim_df = model_data["similarity_matrix"][product.description].sort_values(
            ascending=False
        )
        rec_descriptions = sim_df.iloc[1:11].index.tolist()

    recommendations = []
    if rec_descriptions:
        recs = (
            db.session.query(
                Transaction.stock_code,
                func.max(Transaction.description).label("description"),
                func.max(Transaction.unit_price).label("unit_price"),
            )
            .filter(Transaction.description.in_(rec_descriptions))
            .group_by(Transaction.stock_code)
            .all()
        )
        rec_map = {r.description: r for r in recs}
        for desc in rec_descriptions:
            if desc in rec_map:
                r = rec_map[desc]
                recommendations.append(
                    {
                        "stock_code": r.stock_code,
                        "description": r.description,
                        "unit_price": r.unit_price,
                        "image_url": f"https://picsum.photos/seed/{r.stock_code}/300/300",
                    }
                )
    else:
        recs = (
            db.session.query(
                Transaction.stock_code,
                func.max(Transaction.description).label("description"),
                func.max(Transaction.unit_price).label("unit_price"),
            )
            .filter(Transaction.stock_code != stock_code)
            .group_by(Transaction.stock_code)
            .order_by(func.random())
            .limit(10)
            .all()
        )
        for r in recs:
            recommendations.append(
                {
                    "stock_code": r.stock_code,
                    "description": r.description,
                    "unit_price": r.unit_price,
                    "image_url": f"https://picsum.photos/seed/{r.stock_code}/300/300",
                }
            )

    return render_template(
        "product.html",
        product={
            "stock_code": product.stock_code,
            "description": product.description,
            "unit_price": product.unit_price,
            "image_url": f"https://picsum.photos/seed/{product.stock_code}/400/400",
            "recommendations": recommendations,
        },
    )


@app.route("/api/users")
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="127.0.0.1", port=port, debug=debug)

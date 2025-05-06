from flask import Blueprint, request, jsonify
from .models import db, User, Item, CartItem, Checkout, CheckoutStatusEnum
#from .tasks import process_checkout
from datetime import datetime
import time

bp = Blueprint("api", __name__)

# Track processing time (in-memory, not persistent)
checkout_times = {}  # {checkout_id: (start_time, end_time)}

# 1. Add to Cart
@bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get("user_id")
    item_id = data.get("item_id")
    quantity = data.get("quantity")

    if not all([user_id, item_id, quantity]):
        return jsonify({"error": "Missing fields"}), 400

    cart_item = CartItem(user_id=user_id, item_id=item_id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()

    return jsonify({"message": "Item added to cart"}), 201

# 2. Initiate Checkout
@bp.route('/checkout', methods=['POST'])
def initiate_checkout():
    from .tasks import process_checkout  # ✅ Move import here to avoid circular import

    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    checkout = Checkout(user_id=user_id, status=CheckoutStatusEnum.pending)
    db.session.add(checkout)
    db.session.commit()

    checkout_times[checkout.id] = (time.time(), None)

    # Trigger background processing
    process_checkout.delay(checkout.id)

    return jsonify({"checkout_id": checkout.id, "status": "Pending"}), 202

# 3. Get Checkout Status
@bp.route('/checkout/<int:checkout_id>/status', methods=['GET'])
def get_checkout_status(checkout_id):
    checkout = Checkout.query.get(checkout_id)
    if not checkout:
        return jsonify({"error": "Checkout not found"}), 404
    return jsonify({"checkout_id": checkout.id, "status": checkout.status.value})

# 4. Metrics
@bp.route('/metrics', methods=['GET'])
def metrics():
    checkouts = Checkout.query.all()
    total = len(checkouts)
    status_counts = {"Pending": 0, "Processing": 0, "Completed": 0}
    times = []

    for c in checkouts:
        status_counts[c.status.value] += 1
        if checkout_times.get(c.id) and checkout_times[c.id][1]:
            start, end = checkout_times[c.id]
            times.append(end - start)

    avg_time = round(sum(times) / len(times), 2) if times else 0

    return jsonify({
        "total_checkouts_processed": total,
        "average_processing_time_seconds": avg_time,
        "checkout_status_counts": status_counts
    })


@bp.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(id=data["id"], name=data["name"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@bp.route("/item", methods=["POST"])
def create_item():
    data = request.get_json()
    item = Item(id=data["id"], name=data["name"], price=data["price"])
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Item created"}), 201

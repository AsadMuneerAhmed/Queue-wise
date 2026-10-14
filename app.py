
from datetime import datetime, date
from math import ceil
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, instance_relative_config=True)
Path(app.instance_path).mkdir(parents=True, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + str(Path(app.instance_path) / "queuewise.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

SERVICE_TIME_MINUTES = 8


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_number = db.Column(db.String(20), nullable=False)
    visitor_name = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Waiting", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    called_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    counter_id = db.Column(db.Integer, db.ForeignKey("counter.id"), nullable=True)
    counter = db.relationship("Counter", backref="tokens")


def active_counters():
    return Counter.query.filter_by(is_active=True).count()


def estimate_wait(position):
    counters = active_counters()
    if position <= 0:
        return 0
    return ceil(position * SERVICE_TIME_MINUTES / max(counters, 1))


def token_to_dict(token):
    waiting_tokens = (
        Token.query.filter_by(status="Waiting")
        .filter(Token.created_at <= token.created_at)
        .order_by(Token.created_at, Token.id)
        .all()
    )

    position = 0
    if token.status == "Waiting":
        for index, waiting_token in enumerate(waiting_tokens, start=1):
            if waiting_token.id == token.id:
                position = index
                break

    return {
        "id": token.id,
        "token_number": token.token_number,
        "visitor_name": token.visitor_name,
        "service": token.service,
        "status": token.status,
        "position": position,
        "estimated_wait_minutes": estimate_wait(position),
        "counter": token.counter.name if token.counter else None,
        "created_at": token.created_at.isoformat(timespec="minutes"),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/staff")
def staff_dashboard():
    return render_template("staff.html")


@app.route("/token/<int:token_id>")
def token_page(token_id):
    token = db.session.get(Token, token_id)
    if token is None:
        return "Token not found", 404
    return render_template("token.html", token=token)


@app.get("/api/health")
def health():
    return jsonify({"status": "online", "app": "QueueWise"})


@app.post("/api/tokens")
def create_token():
    data = request.get_json(silent=True) or {}

    visitor_name = str(data.get("visitor_name", "")).strip()
    service = str(data.get("service", "")).strip()

    if not visitor_name or not service:
        return jsonify({
            "error": "Visitor name and service are required."
        }), 400

    if len(visitor_name) > 100 or len(service) > 100:
        return jsonify({"error": "Input is too long."}), 400

    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    tomorrow_start = datetime.combine(
        date.fromordinal(today.toordinal() + 1),
        datetime.min.time()
    )

    todays_count = Token.query.filter(
        Token.created_at >= today_start,
        Token.created_at < tomorrow_start
    ).count()

    token_number = f"Q{todays_count + 1:03d}"

    token = Token(
        token_number=token_number,
        visitor_name=visitor_name,
        service=service,
    )

    db.session.add(token)
    db.session.commit()

    return jsonify({
        "message": "Queue token created successfully.",
        "token": token_to_dict(token),
    }), 201


@app.get("/api/queue")
def get_queue():
    waiting = Token.query.filter_by(status="Waiting").order_by(
        Token.created_at, Token.id
    ).all()

    serving = Token.query.filter_by(status="Serving").order_by(
        Token.called_at, Token.id
    ).all()

    return jsonify({
        "waiting": [token_to_dict(token) for token in waiting],
        "serving": [token_to_dict(token) for token in serving],
        "active_counters": active_counters(),
    })


@app.get("/api/tokens/<int:token_id>")
def get_token(token_id):
    token = db.session.get(Token, token_id)
    if token is None:
        return jsonify({"error": "Token not found."}), 404

    return jsonify({"token": token_to_dict(token)})



@app.post("/api/staff/next")
def call_next_token():
    data = request.get_json(silent=True) or {}
    counter_id = data.get("counter_id")

    # If a counter ID is supplied, preserve manual counter selection.
    if counter_id is not None:
        try:
            counter_id = int(counter_id)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid counter ID."}), 400

        counter = db.session.get(Counter, counter_id)

        if counter is None or not counter.is_active:
            return jsonify({"error": "Active counter not found."}), 404

        already_serving = Token.query.filter_by(
            status="Serving",
            counter_id=counter.id
        ).first()

        if already_serving:
            return jsonify({
                "error": f"{counter.name} is already serving a token."
            }), 409

    else:
        # SMART ASSIGNMENT:
        # Find active counters that are currently available.
        active = Counter.query.filter_by(
            is_active=True
        ).order_by(Counter.id).all()

        available_counters = []

        for item in active:
            current_token = Token.query.filter_by(
                status="Serving",
                counter_id=item.id
            ).first()

            if current_token is None:
                available_counters.append(item)

        if not available_counters:
            if not active:
                return jsonify({
                    "error": "No active counters. Activate a counter first."
                }), 400

            return jsonify({
                "error": "All active counters are busy. Complete a service first."
            }), 409

        # Count completed services today to balance workload.
        today = date.today()
        today_start = datetime.combine(today, datetime.min.time())
        tomorrow_start = datetime.combine(
            date.fromordinal(today.toordinal() + 1),
            datetime.min.time()
        )

        def completed_today(item):
            return Token.query.filter(
                Token.counter_id == item.id,
                Token.status == "Completed",
                Token.completed_at >= today_start,
                Token.completed_at < tomorrow_start
            ).count()

        # Lowest workload first; Counter ID breaks ties.
        counter = min(
            available_counters,
            key=lambda item: (completed_today(item), item.id)
        )

    # Assign the oldest waiting visitor to the chosen counter.
    token = Token.query.filter_by(
        status="Waiting"
    ).order_by(
        Token.created_at,
        Token.id
    ).first()

    if token is None:
        return jsonify({"error": "No waiting tokens."}), 404

    token.status = "Serving"
    token.called_at = datetime.now()
    token.counter_id = counter.id

    db.session.commit()

    return jsonify({
        "message": f"{token.token_number} assigned to {counter.name}.",
        "assignment_mode": (
            "manual" if counter_id is not None else "smart"
        ),
        "token": token_to_dict(token),
        "counter": {
            "id": counter.id,
            "name": counter.name
        }
    })

@app.post("/api/tokens/<int:token_id>/complete")
def complete_token(token_id):
    token = db.session.get(Token, token_id)

    if token is None:
        return jsonify({"error": "Token not found."}), 404

    if token.status != "Serving":
        return jsonify({
            "error": "Only a token currently being served can be completed."
        }), 400

    token.status = "Completed"
    token.completed_at = datetime.now()
    db.session.commit()

    return jsonify({
        "message": "Service completed.",
        "token": token_to_dict(token),
    })


@app.get("/api/counters")
def get_counters():
    counters = Counter.query.order_by(Counter.id).all()
    result = []

    for counter in counters:
        current_token = Token.query.filter_by(
            counter_id=counter.id,
            status="Serving"
        ).first()

        result.append({
            "id": counter.id,
            "name": counter.name,
            "is_active": counter.is_active,
            "serving": (
                current_token.token_number
                if current_token else None
            ),
        })

    return jsonify({"counters": result})
@app.post("/api/counters")
def create_counter():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()

    if not name:
        return jsonify({"error": "Counter name is required."}), 400

    if len(name) > 80:
        return jsonify({"error": "Counter name is too long."}), 400

    counter = Counter(name=name, is_active=True)
    db.session.add(counter)
    db.session.commit()

    return jsonify({
        "message": "Counter created.",
        "counter": {
            "id": counter.id,
            "name": counter.name,
            "is_active": counter.is_active,
        },
    }), 201


@app.patch("/api/counters/<int:counter_id>")
def update_counter(counter_id):
    counter = db.session.get(Counter, counter_id)

    if counter is None:
        return jsonify({"error": "Counter not found."}), 404

    data = request.get_json(silent=True) or {}

    if "is_active" in data:
        if not isinstance(data["is_active"], bool):
            return jsonify({"error": "is_active must be true or false."}), 400

        if not data["is_active"] and Token.query.filter_by(
            counter_id=counter.id, status="Serving"
        ).first():
            return jsonify({
                "error": "Complete the current token before deactivating this counter."
            }), 409

        counter.is_active = data["is_active"]

    if "name" in data:
        name = str(data["name"]).strip()
        if not name or len(name) > 80:
            return jsonify({"error": "Enter a valid counter name."}), 400
        counter.name = name

    db.session.commit()

    return jsonify({
        "message": "Counter updated.",
        "counter": {
            "id": counter.id,
            "name": counter.name,
            "is_active": counter.is_active,
        },
    })


@app.get("/api/analytics")
def analytics():
    total = Token.query.count()
    waiting = Token.query.filter_by(status="Waiting").count()
    serving = Token.query.filter_by(status="Serving").count()
    completed = Token.query.filter_by(status="Completed").count()

    completed_tokens = Token.query.filter(
        Token.status == "Completed",
        Token.called_at.isnot(None),
        Token.completed_at.isnot(None),
    ).all()

    wait_durations = [
        (token.called_at - token.created_at).total_seconds() / 60
        for token in completed_tokens
    ]

    average_wait = (
        round(sum(wait_durations) / len(wait_durations), 1)
        if wait_durations else 0
    )

    return jsonify({
        "total_tokens": total,
        "waiting": waiting,
        "serving": serving,
        "completed": completed,
        "active_counters": active_counters(),
        "average_wait_minutes": average_wait,
    })


with app.app_context():
    db.create_all()

    if Counter.query.count() == 0:
        db.session.add_all([
            Counter(name="Counter 1"),
            Counter(name="Counter 2"),
        ])
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
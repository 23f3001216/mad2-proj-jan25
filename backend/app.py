from flask import Blueprint, request, jsonify
from flask_app import create_app
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, Admin, User, ParkingLot, ParkingSpot, Reservation
import pytz
from math import ceil
from celery_app import celery
from tasks import export_user_reservations, send_daily_reminders, send_monthly_report


IST = pytz.timezone('Asia/Kolkata')

app, login_manager = create_app()

@login_manager.user_loader
def load_user(user_id):
    if user_id.startswith("user-"):
        user = User.query.get(int(user_id.split("-")[1]))
        if user:
            user._role = "user"
            return user

    elif user_id.startswith("admin-"):
        admin = Admin.query.get(int(user_id.split("-")[1]))
        if admin:
            admin._role = "admin"
            return admin

    return None

# --- Root Route ---
@app.route('/')
def index():
    return {"status": "Backend is running"}

# --- Auth Blueprint ---
auth_bp = Blueprint('auth', __name__)

@app.route("/whoami")
@login_required
def whoami():
    return jsonify({
        "id": current_user.id,
        "role": getattr(current_user, '_role', 'unknown'),
        "name": getattr(current_user, 'full_name', 'Admin')
    })

# ------------------ User Register ------------------
@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        required_fields = ['full_name', 'email', 'password', 'address', 'pincode']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "User already exists"}), 400

        user = User(
            full_name=data['full_name'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            address=data['address'],
            pincode=data['pincode']
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ User Login ------------------
@auth_bp.route('/user-login', methods=['POST'])
def login_user_route():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({"error": "Invalid credentials"}), 401

        login_user(user)
        return jsonify({"message": "User logged in", "role": "user", "id": user.id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ Admin Login ------------------
@auth_bp.route('/admin-login', methods=['POST'])
def login_admin():
    try:
        data = request.get_json()
        admin = Admin.query.filter_by(username=data['username']).first()
        if not admin or not check_password_hash(admin.password, data['password']):
            return jsonify({"error": "Invalid credentials"}), 401

        login_user(admin)
        return jsonify({"message": "Admin logged in", "role": "admin"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ Logout ------------------
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route('/api/admin/profile', methods=['PUT'])
@login_required
def update_admin_profile():
    if not isinstance(current_user, Admin):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    new_password = data.get("new_password", "").strip()

    if new_password:
        from werkzeug.security import generate_password_hash
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"message": "Password updated"}), 200
    else:
        return jsonify({"error": "Password is required"}), 400

# --- Get all parking lots ---
@auth_bp.route('/api/parking-lots', methods=['GET'])
def get_parking_lots():
    lots = ParkingLot.query.all()
    return jsonify([{
        "id": lot.id,
        "name": lot.name,
        "address": lot.address,
        "pincode": lot.pincode,
        "price": lot.price_per_hour,
        "totalSpots": lot.total_spots,
        "spots": [{"id": spot.id, "status": spot.status} for spot in lot.spots]
    } for lot in lots])

# --- Create a new parking lot ---
@auth_bp.route('/api/parking-lots', methods=['POST'])
def create_parking_lot():
    data = request.get_json()

    new_lot = ParkingLot(
        name=data['name'],
        address=data['address'],
        pincode=data['pincode'],
        price_per_hour=data['price'],
        total_spots=data['maxSpots']
    )
    db.session.add(new_lot)
    db.session.flush()  

    for _ in range(data['maxSpots']):
        db.session.add(ParkingSpot(status='A', lot_id=new_lot.id))

    db.session.commit()
    return jsonify({"message": "Parking lot created successfully"}), 201

# --- Update parking lot ---
@auth_bp.route('/api/parking-lots/<int:lot_id>', methods=['PUT'])
def update_parking_lot(lot_id):
    data = request.get_json()
    lot = ParkingLot.query.get_or_404(lot_id)

    lot.name = data['name']
    lot.address = data['address']
    lot.pincode = data['pincode']
    lot.price_per_hour = data['price']
    db.session.commit()

    return jsonify({"message": "Parking lot updated successfully"})

# --- Delete parking lot (only if all spots are empty) ---
@auth_bp.route('/api/parking-lots/<int:lot_id>', methods=['DELETE'])
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    occupied = any(spot.status == 'O' for spot in lot.spots)
    if occupied:
        return jsonify({"error": "Cannot delete. Some spots are occupied."}), 400

    db.session.delete(lot)
    db.session.commit()
    return jsonify({"message": "Parking lot deleted successfully"})

# --- Get all users ---
@auth_bp.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'email': user.email,
            'name': user.full_name,
            'address': user.address,
            'pin': user.pincode
        } for user in users
    ])

@auth_bp.route('/api/admin/summary', methods=['GET'])
def get_admin_summary():
    lots = ParkingLot.query.all()
    revenue_summary = []
    total_available = total_occupied = 0

    for lot in lots:
        total_revenue = 0
        for spot in lot.spots:
            for reservation in spot.reservations:
                if reservation.left_at:
                    duration = reservation.left_at - reservation.parked_at
                    hours = ceil(duration.total_seconds() / 3600)
                    total_revenue += hours * lot.price_per_hour
        revenue_summary.append({
            'name': lot.name,
            'totalRevenue': total_revenue,
        })

        for spot in lot.spots:
            if spot.status == 'A':
                total_available += 1
            elif spot.status == 'O':
                total_occupied += 1

    return jsonify({
        'revenue': revenue_summary,
        'occupancy': {
            'available': total_available,
            'occupied': total_occupied,
            'total': total_available + total_occupied,
        }
    })

@auth_bp.route('/api/parking-lots/<int:lot_id>/spots', methods=['POST'])
def add_parking_spot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    new_spot = ParkingSpot(status='A', lot_id=lot.id)
    db.session.add(new_spot)
    db.session.commit()
    return jsonify({"message": "Spot added", "spotId": new_spot.id}), 201

@auth_bp.route('/api/parking-spots/<int:spot_id>', methods=['DELETE'])
def delete_parking_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.status != 'A':
        return jsonify({"error": "Cannot delete occupied spot"}), 400
    db.session.delete(spot)
    db.session.commit()
    return jsonify({"message": "Spot deleted"}), 200

@auth_bp.route('/api/search-parking')
def search_parking():
    search_by = request.args.get('by')
    search_text = request.args.get('text', '').lower()

    if not search_text:
        return jsonify({'type': '', 'data': []})

    if search_by == 'location':
        lots = ParkingLot.query.filter(ParkingLot.address.ilike(f"%{search_text}%")).all()
        data = []
        for lot in lots:
            data.append({
                'id': lot.id,
                'name': lot.name,
                'address': lot.address,
                'pincode': lot.pincode,
                'price': lot.price_per_hour,
                'spots': [{'id': spot.id, 'status': spot.status} for spot in lot.spots],
            })
        return jsonify({'type': 'parking_lots', 'data': data})

    elif search_by == 'user':
        # Search by ID or name (partial case-insensitive match)
        if search_text.isdigit():
            users = User.query.filter(User.id == int(search_text)).all()
        else:
            users = User.query.filter(User.full_name.ilike(f"%{search_text}%")).all()

        data = [
            {
                'id': user.id,
                'name': user.full_name,
                'email': user.email,
                'address': user.address,
                'pin': user.pincode,
            }
            for user in users
        ]
        return jsonify({'type': 'user', 'data': data})

    return jsonify({'type': '', 'data': []})

@auth_bp.route('/api/user/lots')
@login_required
def get_lots():
    query = request.args.get('search', '').lower()
    lots = ParkingLot.query.filter(ParkingLot.address.ilike(f"%{query}%")).all()
    result = []
    for lot in lots:
        result.append({
            'id': lot.id,
            'address': lot.address,
            'spots': [{'id': s.id, 'status': s.status} for s in lot.spots],
        })
    return jsonify(result)


@auth_bp.route('/api/user/book', methods=['POST'])
@login_required
def book_spot():
    data = request.get_json()
    lot_id = data.get('lotId')
    vehicle_no = data.get('vehicleNo')

    if not lot_id or not vehicle_no:
        return jsonify({'error': 'Missing lot ID or vehicle number'}), 400

    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({'error': 'Invalid parking lot'}), 404

    # Find the first available spot
    spot = next((s for s in lot.spots if s.status == 'A'), None)
    if not spot:
        return jsonify({'error': 'No available spots'}), 400

    # Update spot status and create reservation
    spot.status = 'O'
    reservation = Reservation(
        user_id=current_user.id,
        spot_id=spot.id,
        parked_at=datetime.now(IST),
        left_at=None,
        cost=0.0,
        vehicle_number=vehicle_no
    )
    db.session.add(reservation)
    db.session.commit()

    return jsonify({'message': 'Reservation successful'})


@auth_bp.route('/api/user/release', methods=['POST'])
@login_required
def release_spot():
    res_id = request.json['id']
    reservation = Reservation.query.get(res_id)

    if not reservation or reservation.user_id != current_user.id:
        return jsonify({'error': 'Invalid reservation'}), 404

    now = datetime.now(IST)

    # Convert both to timezone-aware consistently
    parked_at = reservation.parked_at
    if parked_at.tzinfo is None:
        parked_at = IST.localize(parked_at)

    left_at = now
    reservation.left_at = left_at

    # Calculate duration in hours (ceil to next hour)
    duration = left_at - parked_at
    duration_hours = ceil(duration.total_seconds() / 3600)

    # Set cost and free the spot
    reservation.cost = duration_hours * reservation.spot.lot.price_per_hour
    reservation.spot.status = 'A'
    db.session.commit()

    return jsonify({'message': 'Spot released'})


@auth_bp.route('/api/user/reservations')
@login_required
def user_history():
    res = Reservation.query.filter_by(user_id=current_user.id).all()
    data = []
    for r in res:
        data.append({
            'id': r.id,
            'location': r.spot.lot.address,
            'vehicleNo': r.vehicle_number,
            'timestamp': r.parked_at.strftime("%d-%m-%Y %I:%M %p"),
            'status': 'O' if r.left_at is None else 'R',
            'parkingTime': r.parked_at.strftime("%d-%m-%Y %I:%M %p"),
            'releasingTime': r.left_at.strftime("%d-%m-%Y %I:%M %p") if r.left_at else '',
            'totalCost': f"₹{r.cost:.2f}" if r.left_at else '',
            'spotId': r.spot.id,
        })

    return jsonify(data)

@auth_bp.route("/api/user/summary")
@login_required
def get_user_chart_summary():
    # Ensure the current user is actually a User (not Admin)
    if not hasattr(current_user, 'reservations'):
        return jsonify({"error": "Unauthorized access"}), 403

    completed = sum(1 for r in current_user.reservations if r.left_at is not None)
    ongoing = sum(1 for r in current_user.reservations if r.left_at is None)

    return jsonify({
        "active": ongoing,
        "completed": completed
    }), 200

# --- Get user profile ---
@auth_bp.route('/api/user/profile', methods=['GET'])
@login_required
def get_user_profile():
    if not isinstance(current_user, User):
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify({
        "full_name": current_user.full_name,
        "address": current_user.address,
        "pincode": current_user.pincode
    }), 200

# --- Update user profile ---
@auth_bp.route('/api/user/profile', methods=['PUT'])
@login_required
def update_user_profile():
    if not isinstance(current_user, User):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    current_user.full_name = data.get("full_name", current_user.full_name)
    current_user.address = data.get("address", current_user.address)
    current_user.pincode = data.get("pincode", current_user.pincode)

    new_password = data.get("new_password", "").strip()
    if new_password:
        from werkzeug.security import generate_password_hash
        current_user.password = generate_password_hash(new_password)

    db.session.commit()
    return jsonify({"message": "Profile updated"}), 200

@auth_bp.route("/api/export-csv", methods=["POST"])
@login_required
def export_csv():
    task = export_user_reservations.delay(current_user.id)
    return jsonify({"message": "CSV export started", "task_id": task.id}), 202

@auth_bp.route("/api/run-daily-reminder", methods=["GET"])
def run_daily_reminder():
    send_daily_reminders.delay()
    return jsonify({"message": "Daily reminder triggered"}), 200

@auth_bp.route("/api/run-monthly-report", methods=["GET"])
def run_monthly_report():
    send_monthly_report.delay()
    return jsonify({"message": "Monthly report triggered"}), 200

# Register Blueprint
app.register_blueprint(auth_bp)

# ------------------ DB Init & Seed Admin ------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin', password=generate_password_hash("admin123"))
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
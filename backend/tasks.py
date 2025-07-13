from datetime import datetime
from celery_app import celery
import os, csv
from models import db, User, Reservation, ParkingLot
from flask_app import create_app
app, _ = create_app()
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from calendar import monthrange
from dotenv import load_dotenv

load_dotenv()  

def send_email(to_email, subject, body, html=False):
    from_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASS")

    msg = MIMEText(body, 'html' if html else 'plain')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, app_password)
            server.sendmail(from_email, to_email, msg.as_string())
    except Exception as e:
        print("Email failed:", str(e))

@celery.task(name="tasks.export_user_reservations")
def export_user_reservations(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        if not user:
            return f"User {user_id} not found."

        reservations = user.reservations

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        os.makedirs("exports", exist_ok=True)
        filename = f"exports/reservations_user_{user_id}_{timestamp}.csv"

        try:
            with open(filename, mode="w", newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Reservation ID", "Spot ID", "Lot Name", "Lot Address", 
                    "Parked At", "Left At", "Cost"
                ])
                for r in reservations:
                    lot = r.spot.lot
                    writer.writerow([
                        r.id,
                        r.spot_id,
                        lot.name,
                        lot.address,
                        r.parked_at.strftime("%d-%m-%Y %H:%M"),
                        r.left_at.strftime("%d-%m-%Y %H:%M") if r.left_at else "Still Parked",
                        f"₹{r.cost:.2f}" if r.cost else "Pending"
                    ])
            return f"CSV exported: {filename}"
        except Exception as e:
            return f"Export failed: {str(e)}"
        
@celery.task(name="tasks.send_daily_reminders")
def send_daily_reminders():
    with app.app_context():
        all_users = User.query.all()
        for user in all_users:
            has_reservations_today = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.parked_at >= datetime.now().replace(hour=0, minute=0, second=0)
            ).count() > 0

            if not has_reservations_today:
                print(f"Sending reminder to {user.email}")
                send_email(
                    user.email,
                    subject="🚗 Don't forget to reserve your parking spot!",
                    body = """
                            <html>
                            <body style="font-family:Arial, sans-serif; background-color:#f4f6f8; padding:20px;">
                                <div style="max-width:600px; margin:auto; background-color:#ffffff; padding:30px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.05);">
                                <h2 style="color:#d81b60; margin-bottom:20px;">⏰ Parking Reminder</h2>
                                <p>Hi there,</p>
                                <p>This is a gentle reminder from <strong>ParkPal</strong> — it looks like you haven’t reserved a parking spot today.</p>
                                <p>To ensure you have a hassle-free parking experience, we recommend booking early.</p>
                                <div style="text-align:center; margin-top:30px;">
                                    <a href="http://localhost:5173/user/home" 
                                    style="background-color:#d81b60; color:white; padding:12px 24px; text-decoration:none; border-radius:6px; font-weight:bold;">
                                    Reserve Now
                                    </a>
                                </div>
                                <p style="margin-top:40px;">Safe parking,<br><strong>The ParkPal Team</strong></p>
                                <hr style="margin-top:30px;">
                                <p style="font-size:12px; color:#999;">This is an automated message from ParkPal. Please do not reply to this email.</p>
                                </div>
                            </body>
                            </html>
                            """,
                    html=True
                )

from calendar import monthrange

@celery.task(name="tasks.send_monthly_report")
def send_monthly_report():
    with app.app_context():
        today = datetime.now()
        first_day_this_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day_prev_month = first_day_this_month - timedelta(seconds=1)
        first_day_prev_month = last_day_prev_month.replace(day=1)

        users = User.query.all()

        for user in users:
            reservations = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.parked_at >= first_day_prev_month,
                Reservation.parked_at <= last_day_prev_month
            ).all()

            if not reservations:
                continue  

            lot_count = {}
            total_spent = 0
            for r in reservations:
                lot = r.spot.lot
                lot_count[lot.name] = lot_count.get(lot.name, 0) + 1
                total_spent += r.cost or 0

            most_used = max(lot_count, key=lot_count.get) if lot_count else "N/A"

            html_body = f"""
            <html>
            <body style="font-family:Arial, sans-serif; background-color:#fff5f7; padding:20px;">
                <div style="max-width:600px; margin:auto; background-color:#ffffff; padding:30px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.05);">
                    <h2 style="color:#e91e63; margin-bottom:20px;">📊 Your Monthly Parking Summary</h2>
                    <p>Dear {user.full_name},</p>
                    <p>Thank you for using <strong>ParkPal</strong> last month. Here's a quick overview of your parking activity for {first_day_prev_month.strftime("%B %Y")}:</p>

                    <table style="width:100%; border-collapse:collapse; margin-top:20px; font-size:15px;">
                        <tr style="background-color:#fce4ec;">
                            <td style="padding:12px; font-weight:bold;">Total Reservations</td>
                            <td style="padding:12px;">{len(reservations)}</td>
                        </tr>
                        <tr>
                            <td style="padding:12px; font-weight:bold;">Most Used Parking Lot</td>
                            <td style="padding:12px;">{most_used}</td>
                        </tr>
                        <tr style="background-color:#fce4ec;">
                            <td style="padding:12px; font-weight:bold;">Total Amount Spent</td>
                            <td style="padding:12px;">₹{total_spent:.2f}</td>
                        </tr>
                    </table>

                    <p style="margin-top:30px;">We appreciate your continued trust in ParkPal. If you have any feedback or questions, we'd love to hear from you.</p>

                    <p style="margin-top:40px;">Warm regards,<br><strong>The ParkPal Team</strong></p>
                    <hr style="margin-top:30px;">
                    <p style="font-size:12px; color:#999;">This report was automatically generated by ParkPal. Please do not reply to this message.</p>
                </div>
            </body>
            </html>
            """

            send_email(user.email, f"📊 Your {first_day_prev_month.strftime('%B %Y')} Parking Report", html_body, html=True)

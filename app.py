from flask import Flask, render_template, request, session, redirect, url_for, flash
import smtplib, os, random
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "your_secret_key"   # needed for sessions

# Email config (set in Render → Environment Variables)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")   # your Gmail
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") # your Gmail App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Store OTPs temporarily
otp_storage = {}

def send_otp_email(to_email, otp):
    subject = "Your OTP Verification Code"
    body = f"Your OTP code is {otp}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp
        session["email"] = email
        send_otp_email(email, otp)
        flash("OTP has been sent to your email")
        return redirect(url_for("verify"))
    return render_template("register.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        user_otp = request.form["otp"]
        email = session.get("email")
        if email and otp_storage.get(email) == user_otp:
            flash("✅ Email verified successfully!")
            otp_storage.pop(email, None)
            return redirect(url_for("register"))
        else:
            flash("❌ Invalid OTP, try again")
    return render_template("verify.html")

if __name__ == "__main__":
    app.run(debug=True)

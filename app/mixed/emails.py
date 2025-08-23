import random
from flask import render_template
from app.new_file import db
from app import mail
from app.models import User, Verification
from flask_mail import Message
from flask_login import current_user

def verification_email(user_email: str) -> bool:
    user = User.query.filter_by(email = user_email).first()
    if not user:
        code = ''.join(random.choices("0123456789", k=6))
        verified = Verification(email=user_email, verification_code = code)
        #user = Verification(email=user_email)
        db.session.add(verified)
        #db.session.add(user)
        db.session.commit()
        html = render_template("email_verify.html", code=code)
        msg = Message(
            sender= "chenyingshu1234@gmail.com",
            subject="Please confirm your email",
            recipients=[user_email],
            html=html,
        )
        mail.send(msg)
        return True
    else:
        return False

def confirmation_email(id: int):
    emails = db.session.query(User).filter_by(role = "Admin").all()
    if emails:
        html = render_template("confirmation_sent.html", user = current_user.username, id = id)
        for email in emails:
            msg = Message(sender="chenyingshu1234@gmail.com",
                          subject="A new edit or addition",
                          recipients = [email.email],
                          html=html,)
            mail.send(msg)


def new_confirmation_email(id: int, category: str):
    emails = db.session.query(User).filter_by(role = "Admin").all()
    if emails:
        html = render_template("confirmation_sent.html", user = current_user.username, id = id, category =category)
        for email in emails:
            msg = Message(sender="chenyingshu1234@gmail.com",
                          subject="A new image edit or addition",
                          recipients = [email.email],
                          html=html,)
            mail.send(msg)



def approval_email(user_email: str, emperor_title: str):
        html = render_template("approval_sent.html", title = emperor_title )
        msg = Message(sender="chenyingshu1234@gmail.com",
                          subject="Approval",
                          recipients = [user_email],
                          html=html,)
        mail.send(msg)



def rejection_email(user_email: str, emperor_title: str):
        html = render_template("rejection.sent.html", title = emperor_title )
        msg = Message(sender="chenyingshu1234@gmail.com",
                          subject="Rejection",
                          recipients = [user_email],
                          html=html,)
        mail.send(msg)


from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped
from werkzeug.security import generate_password_hash, check_password_hash
from app.new_file import db, login
from dataclasses import dataclass
import datetime
from datetime import datetime, timezone

@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True, nullable=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=True)
    #verification_code: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True, nullable=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable=True)
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="Normal", nullable=True)
    user_type: Mapped[str] = so.mapped_column(sa.String(64), default="user")
    invitations: so.Mapped[list['Invitation']] = relationship(back_populates='user', cascade='all, delete-orphan')
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type
    }


    def __repr__(self):
        pwh= 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))





class Verification(db.Model):
    __tablename__ = 'verification'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    verification_code: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True, nullable=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, nullable=True)
    created_at: so.Mapped[str] = so.mapped_column(sa.String(256), default=lambda:datetime.now(timezone.utc).isoformat())



class Emperor(db.Model):
    __tablename__ = 'emperors'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True)
    in_greek: so.Mapped[str] = so.mapped_column(sa.String(256))
    birth: so.Mapped[str] = so.mapped_column(sa.String(256))
    death: so.Mapped[str] = so.mapped_column(sa.String(256))
    reign: so.Mapped[str] = so.mapped_column(sa.String(256))
    dynasty: so.Mapped[str] = so.mapped_column(sa.String(256))
    first_reign: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    second_reign: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    life: so.Mapped[str] = so.mapped_column(sa.Text())
    images: so.Mapped[list["Image"]] = so.relationship(back_populates="emperor", cascade="all, delete-orphan")



class Image(db.Model):
    __tablename__ = 'images'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    filename: so.Mapped[str] = so.mapped_column(sa.String(256))
    url: so.Mapped[str] = so.mapped_column(sa.Text())
    caption: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    emperor_title: so.Mapped[str] = so.mapped_column(sa.ForeignKey("emperors.title"), nullable=True)
    emperor: so.Mapped["Emperor"] = so.relationship(back_populates="images", foreign_keys=[emperor_title])



class Invitation(db.Model):
    __tablename__ = 'invitations'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    code: so.Mapped[str] = so.mapped_column(sa.String(256))
    user_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey("users.id"), index=True)
    user: so.Mapped["User"] = so.relationship(back_populates="invitations")







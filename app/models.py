from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
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
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable=True)
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="Normal", nullable=True)
    user_type: Mapped[str] = so.mapped_column(sa.String(64), default="user")
    invitations: so.Mapped[list['Invitation']] = relationship(back_populates='user', cascade='all, delete-orphan')
    deletions: so.Mapped[list['Deletion']] = relationship(back_populates='user', cascade='all, delete-orphan')
    active_session: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)

    #def is_admin(self):
        #return self.role == 'Admin'
    #def is_autocrat(self):
        #return self.user_type == 'Autocrat'

    #__mapper_args__ = {
        #"polymorphic_identity": "user",
        #"polymorphic_on": user_type
    #}


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
    reign_start: so.Mapped[int] = so.mapped_column()
    dynasty: so.Mapped[str] = so.mapped_column(sa.String(256))
    ascent_to_power: so.Mapped[str] = so.mapped_column(sa.String(256))
    life: so.Mapped[str] = so.mapped_column(sa.Text())
    references: so.Mapped[str] = so.mapped_column(sa.Text())
    images: so.Mapped[list["Image"]] = so.relationship(back_populates="emperor", cascade="all, delete-orphan")





class Image(db.Model):
    __tablename__ = 'images'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    filename: so.Mapped[str] = so.mapped_column(sa.String(256))
    url: so.Mapped[str] = so.mapped_column(sa.Text())
    caption: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    emperor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("emperors.id"), nullable=True)
    emperor: so.Mapped["Emperor"] = so.relationship(back_populates="images", foreign_keys=[emperor_id])
    war_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("wars.id"), nullable=True)
    war: so.Mapped["War"] = so.relationship(back_populates="images", foreign_keys=[war_id])
    architecture_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("architecture.id"), nullable=True)
    architecture: so.Mapped["Architecture"] = so.relationship(back_populates="images", foreign_keys=[architecture_id])
    literature_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("literature.id"), nullable=True)
    literature: so.Mapped["Literature"] = so.relationship(back_populates="images", foreign_keys=[literature_id])
    artifact_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("artifact.id"), nullable=True)
    artifact: so.Mapped["Artifact"] = so.relationship(back_populates="images", foreign_keys=[artifact_id])


class TemporaryEmperor(db.Model):
    __tablename__ = 'temporary_emperors'
    username: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(256), default="Pending")
    old_id: so.Mapped[int] = so.mapped_column()
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    in_greek: so.Mapped[str] = so.mapped_column(sa.String(256))
    birth: so.Mapped[str] = so.mapped_column(sa.String(256))
    death: so.Mapped[str] = so.mapped_column(sa.String(256))
    reign: so.Mapped[str] = so.mapped_column(sa.String(256))
    ascent_to_power: so.Mapped[str] = so.mapped_column(sa.String(256))
    dynasty: so.Mapped[str] = so.mapped_column(sa.String(256))
    reign_start: so.Mapped[int] = so.mapped_column()
    references: so.Mapped[str] = so.mapped_column(sa.Text())
    created_at: so.Mapped[str] = so.mapped_column(sa.String(256), default=lambda:datetime.now(timezone.utc).isoformat())
    life: so.Mapped[str] = so.mapped_column(sa.Text())
    temporary_images: so.Mapped[list["TemporaryImage"]] = so.relationship(back_populates="temporary_emperor", cascade="all, delete-orphan")





class TemporaryImage(db.Model):
    __tablename__ = 'temporary_images'
    username: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(256), default="Pending")
    old_id: so.Mapped[int] = so.mapped_column()
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    filename: so.Mapped[str] = so.mapped_column(sa.String(256))
    url: so.Mapped[str] = so.mapped_column(sa.Text())
    caption: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    temporary_emperor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("temporary_emperors.id"), nullable=True)
    temporary_emperor: so.Mapped["TemporaryEmperor"] = so.relationship(back_populates="temporary_images", foreign_keys=[temporary_emperor_id])
    temporary_war_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("temporary_wars.id"), nullable=True)
    temporary_war: so.Mapped["TemporaryWar"] = so.relationship(back_populates="temporary_images",
                                                                       foreign_keys=[temporary_war_id])
    temporary_architecture_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("temporary_architecture.id"), nullable=True)
    temporary_architecture: so.Mapped["TemporaryArchitecture"] = so.relationship(back_populates="temporary_images",
                                                               foreign_keys=[temporary_architecture_id])
    temporary_literature_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("temporary_literature.id"),
                                                                 nullable=True)
    temporary_literature: so.Mapped["TemporaryLiterature"] = so.relationship(back_populates="temporary_images",
                                                                                 foreign_keys=[
                                                                                     temporary_literature_id])
    temporary_artifact_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("temporary_artifact.id"),
                                                               nullable=True)
    temporary_artifact: so.Mapped["TemporaryArtifact"] = so.relationship(back_populates="temporary_images",
                                                                             foreign_keys=[
                                                                                 temporary_artifact_id])




class Invitation(db.Model):
    __tablename__ = 'invitations'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    code: so.Mapped[str] = so.mapped_column(sa.String(256))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"), index=True)
    user: so.Mapped["User"] = so.relationship(back_populates="invitations")




class War(db.Model):
    __tablename__ = 'wars'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True)
    start_year: so.Mapped[int] = so.mapped_column()
    dates: so.Mapped[str] = so.mapped_column(sa.String(256))
    location: so.Mapped[str] = so.mapped_column(sa.String(256))
    longitude: so.Mapped[float] = so.mapped_column(nullable=True)
    latitude: so.Mapped[float] = so.mapped_column(nullable=True)
    roman_commanders: so.Mapped[str] = so.mapped_column(sa.String(1024))
    enemy_commanders: so.Mapped[str] = so.mapped_column(sa.String(1024))
    roman_strength: so.Mapped[str] = so.mapped_column(sa.String(1024))
    enemy_strength: so.Mapped[str] = so.mapped_column(sa.String(1024))
    roman_loss: so.Mapped[str] = so.mapped_column(sa.String(1024))
    enemy_loss: so.Mapped[str] = so.mapped_column(sa.String(1024))
    dynasty: so.Mapped[str] = so.mapped_column(sa.String(256))
    war_name: so.Mapped[str] = so.mapped_column(sa.String(256))
    war_type: so.Mapped[str] = so.mapped_column(sa.String(256))
    result: so.Mapped[str] = so.mapped_column(sa.String(256))
    description: so.Mapped[str] = so.mapped_column(sa.Text())
    references: so.Mapped[str] = so.mapped_column(sa.Text())
    images: so.Mapped[list["Image"]] = so.relationship(back_populates="war", cascade="all, delete-orphan")





class TemporaryWar(db.Model):
    __tablename__ = 'temporary_wars'
    username: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(256), default="Pending")
    old_id: so.Mapped[int] = so.mapped_column()
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    start_year: so.Mapped[int] = so.mapped_column()
    dates: so.Mapped[str] = so.mapped_column(sa.String(256))
    location: so.Mapped[str] = so.mapped_column(sa.String(256))
    longitude: so.Mapped[float] = so.mapped_column(nullable=True)
    latitude: so.Mapped[float] = so.mapped_column(nullable=True)
    roman_commanders: so.Mapped[str] = so.mapped_column(sa.String(1024))
    enemy_commanders: so.Mapped[str] = so.mapped_column(sa.String(1024))
    roman_strength: so.Mapped[str] = so.mapped_column(sa.String(1024))
    enemy_strength: so.Mapped[str] = so.mapped_column(sa.String(1024))
    roman_loss: so.Mapped[str] = so.mapped_column(sa.String(1024))
    enemy_loss: so.Mapped[str] = so.mapped_column(sa.String(1024))
    dynasty: so.Mapped[str] = so.mapped_column(sa.String(256))
    war_name: so.Mapped[str] = so.mapped_column(sa.String(256))
    war_type: so.Mapped[str] = so.mapped_column(sa.String(256))
    result: so.Mapped[str] = so.mapped_column(sa.String(256))
    description: so.Mapped[str] = so.mapped_column(sa.Text())
    references: so.Mapped[str] = so.mapped_column(sa.Text())
    created_at: so.Mapped[str] = so.mapped_column(sa.String(256), default=lambda:datetime.now(timezone.utc).isoformat())
    temporary_images: so.Mapped[list["TemporaryImage"]] = so.relationship(back_populates="temporary_war", cascade="all, delete-orphan")




class Architecture(db.Model):
    __tablename__ = 'architecture'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    in_greek: so.Mapped[str] = so.mapped_column(sa.String(256))
    construction_completed: so.Mapped[str] = so.mapped_column(sa.String(256))
    architectural_style: so.Mapped[str] = so.mapped_column(sa.String(256))
    current_status: so.Mapped[str] = so.mapped_column(sa.String(256))
    location: so.Mapped[str] = so.mapped_column(sa.String(256))
    longitude: so.Mapped[float] = so.mapped_column(nullable=True)
    latitude: so.Mapped[float] = so.mapped_column(nullable=True)
    description: so.Mapped[str] = so.mapped_column(sa.Text())
    references: so.Mapped[str] = so.mapped_column(sa.Text())
    building_type: so.Mapped[str] = so.mapped_column(sa.String(256))
    images: so.Mapped[list["Image"]] = so.relationship(back_populates="architecture", cascade="all, delete-orphan")




class TemporaryArchitecture(db.Model):
    __tablename__ = 'temporary_architecture'
    username: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(256), default="Pending")
    old_id: so.Mapped[int] = so.mapped_column()
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    in_greek: so.Mapped[str] = so.mapped_column(sa.String(256))
    construction_completed: so.Mapped[str] = so.mapped_column(sa.String(256))
    architectural_style: so.Mapped[str] = so.mapped_column(sa.String(256))
    current_status:so.Mapped[str] = so.mapped_column(sa.String(256))
    location: so.Mapped[str] = so.mapped_column(sa.String(256))
    longitude: so.Mapped[float] = so.mapped_column(nullable=True)
    latitude: so.Mapped[float] = so.mapped_column(nullable=True)
    description: so.Mapped[str] = so.mapped_column(sa.Text())
    references: so.Mapped[str] = so.mapped_column(sa.Text())
    created_at: so.Mapped[str] = so.mapped_column(sa.String(256), default=lambda:datetime.now(timezone.utc).isoformat())
    building_type: so.Mapped[str] = so.mapped_column(sa.String(256))
    temporary_images: so.Mapped[list["TemporaryImage"]] = so.relationship(back_populates="temporary_architecture", cascade="all, delete-orphan")


class LogBook(db.Model):
    __tablename__ = 'logbooks'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    original_id: so.Mapped[int] = so.mapped_column(nullable=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    username: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    created_at: so.Mapped[str] = so.mapped_column(sa.String(256), default=lambda:datetime.now(timezone.utc).isoformat())


class Version(db.Model):
    __tablename__ = 'versions'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(256))
    unique: so.Mapped[str] = so.mapped_column(sa.String(1024))
    title: so.Mapped[str] = so.mapped_column(sa.String(1024), default=None)
    created_at: so.Mapped[str] = so.mapped_column(sa.String(256))

class CurrentVersion(db.Model):
    __tablename__ = 'current_versions'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(256))
    time_version: so.Mapped[str] = so.mapped_column(sa.String(256))


class NewVersion(db.Model):
    __tablename__ = 'new_versions'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(256))
    time_version: so.Mapped[str] = so.mapped_column(sa.String(256))











class Literature(db.Model):
    __tablename__ = 'literature'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    in_greek: so.Mapped[str] = so.mapped_column(sa.String(256))
    author: so.Mapped[str] = so.mapped_column(sa.String(256))
    year_completed: so.Mapped[str] = so.mapped_column(sa.String(256))
    current_location: so.Mapped[str] = so.mapped_column(sa.String(256))
    genre: so.Mapped[str] = so.mapped_column(sa.String(256))
    description: so.Mapped[str] = so.mapped_column(sa.Text())
    references: so.Mapped[str] = so.mapped_column(sa.Text())
    images: so.Mapped[list["Image"]] = so.relationship(back_populates="literature", cascade="all, delete-orphan")


class TemporaryLiterature(db.Model):
    __tablename__ = 'temporary_literature'
    username: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(256), default="Pending")
    old_id: so.Mapped[int] = so.mapped_column()
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    in_greek: so.Mapped[str] = so.mapped_column(sa.String(256))
    author: so.Mapped[str] = so.mapped_column(sa.String(256))
    year_completed: so.Mapped[str] = so.mapped_column(sa.String(256))
    current_location: so.Mapped[str] = so.mapped_column(sa.String(256))
    genre: so.Mapped[str] = so.mapped_column(sa.String(256))
    description: so.Mapped[str] = so.mapped_column(sa.Text())
    references: so.Mapped[str] = so.mapped_column(sa.Text())
    temporary_images: so.Mapped[list["TemporaryImage"]] = so.relationship(back_populates="temporary_literature", cascade="all, delete-orphan")

class Artifact(db.Model):
    __tablename__ = 'artifact'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    in_greek: so.Mapped[str] = so.mapped_column(sa.String(256))
    year_completed: so.Mapped[str] = so.mapped_column(sa.String(256))
    current_location: so.Mapped[str] = so.mapped_column(sa.String(256))
    description: so.Mapped[str] = so.mapped_column(sa.Text())
    references: so.Mapped[str] = so.mapped_column(sa.Text())
    images: so.Mapped[list["Image"]] = so.relationship(back_populates="artifact", cascade="all, delete-orphan")



class TemporaryArtifact(db.Model):
    __tablename__ = 'temporary_artifact'
    username: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(256), default="Pending")
    old_id: so.Mapped[int] = so.mapped_column()
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    in_greek: so.Mapped[str] = so.mapped_column(sa.String(256))
    year_completed: so.Mapped[str] = so.mapped_column(sa.String(256))
    current_location: so.Mapped[str] = so.mapped_column(sa.String(256))
    description: so.Mapped[str] = so.mapped_column(sa.Text())
    references: so.Mapped[str] = so.mapped_column(sa.Text())
    temporary_images: so.Mapped[list["TemporaryImage"]] = so.relationship(back_populates="temporary_artifact", cascade="all, delete-orphan")



class Deletion(db.Model):
    __tablename__ = 'deletions'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    code: so.Mapped[int] = so.mapped_column()
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"), index=True)
    user: so.Mapped["User"] = so.relationship(back_populates="deletions")

from extensions import db
from flask_login import UserMixin
from datetime import datetime


class Chemical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))
    summary = db.Column(db.Text)
    description = db.Column(db.Text)
    specification = db.Column(db.Text)
    applications = db.Column(db.Text)
    packaging = db.Column(db.Text)
    image_url = db.Column(db.String(300))
    cta_label = db.Column(db.String(120))
    seo_title = db.Column(db.String(200))
    seo_description = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="draft")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Industry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="published")


class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    display_order = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="published")


class SiteSetting(db.Model):
    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Text)


class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200))
    specification = db.Column(db.Text)
    application = db.Column(db.Text)
    quantity = db.Column(db.String(100))
    packaging = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CustomCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    display_order = db.Column(db.Integer, default=0)


class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)

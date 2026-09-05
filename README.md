# GOS Chemicals — Website

A lightweight, professional website for GOS Chemicals — a specialty chemical manufacturer and exporter from India.

## Features

- **Public Website:** Home, Products, Product Detail, Custom Manufacturing, Industries, FAQ, Contact
- **Admin Panel:** Full CRUD for chemicals, industries, FAQs, custom categories, site settings, and contact submission viewer
- **Zero External Setup:** SQLite database auto-created on first run, no Docker/Postgres/cloud DB required
- **Fully Dynamic:** All content served from the database via API — no hardcoded text in the frontend

## Tech Stack

| Layer | Choice |
|---|---|
| Frontend | HTML + CSS + JavaScript (no framework) |
| Backend | Python 3.10+ / Flask |
| Database | SQLite via SQLAlchemy |
| Admin | Server-rendered Jinja2 templates |
| Auth | Flask-Login + bcrypt |

## Quick Start

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env         # macOS/Linux: cp .env.example .env
# Edit .env with your admin email and password
python app.py
```

- **Site:** http://localhost:5000
- **Admin:** http://localhost:5000/admin/login

## Default Admin Credentials

Set in `.env`:
- Email: `admin@goschemicals.com`
- Password: `admin123`

**Change these before deploying to production.**

## Project Structure

```
/backend
  app.py              — Flask entry point
  models.py           — SQLAlchemy models
  seed_data.py        — Starter content (only seeds empty tables)
  config.py           — Configuration from .env
  extensions.py       — db, login_manager instances
  /routes
    api.py            — Public JSON API
    admin.py          — Admin panel CRUD
    auth.py           — Login/logout
  /templates/admin    — Jinja2 admin templates
  /static/uploads     — Product images

/frontend
  index.html          — Home
  products.html       — Product listing
  product-detail.html — Single product (reads ?slug= from URL)
  custom-manufacturing.html
  industries.html
  faq.html
  contact.html
  /css
    tokens.css        — Design tokens (colors, fonts, spacing)
    main.css          — All component styles
  /js
    api.js            — Fetch helpers
    nav.js            — Shared header/footer
    home.js, products.js, product-detail.js, faq.js, industries.js, contact-form.js
```

## Design System

All styling traces back to CSS custom properties in `tokens.css`:
- **Colors:** Warm ivory background, deep forest-green primary, muted gold accents
- **Typography:** Helvetica-based system font stack
- **Spacing:** Generous whitespace, restrained and professional

## Deployment

The backend can be deployed to Render, Railway, or any platform supporting Python/Flask. The frontend is served by the same Flask app — no separate static hosting needed.

For production:
1. Change `SECRET_KEY` to a strong random value
2. Change admin credentials
3. (Optional) Swap local image uploads for Cloudinary by changing how `image_url` is populated

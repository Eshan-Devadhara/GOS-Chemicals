# GOS Chemicals — Website

A lightweight, professional website for GOS Chemicals — a specialty chemical manufacturer and exporter from India.

## Features

- **Public Website:** Home, Products, Product Detail, Custom Manufacturing, Industries, FAQ, Contact
- **Admin Panel:** Full CRUD for chemicals, industries, FAQs, custom categories, site settings, and contact submission viewer
- **Fully Dynamic:** All content served from the database via API — no hardcoded text in the frontend
- **Production-Ready:** PostgreSQL, S3 image uploads, secure sessions, Vercel serverless deployment

## Tech Stack

| Layer | Choice |
|---|---|
| Frontend | HTML + CSS + JavaScript (no framework) |
| Backend | Python 3.10+ / Flask |
| Database | PostgreSQL (production) / SQLite (local dev) |
| File Storage | Amazon S3 (production) / local filesystem (dev) |
| Admin | Server-rendered Jinja2 templates |
| Auth | Flask-Login + bcrypt |
| Deployment | Vercel (Python serverless) |

## Quick Start (Local Development)

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r ../requirements.txt
copy .env.example .env         # macOS/Linux: cp .env.example .env
# Edit .env with your admin email and password
python app.py
```

- **Site:** http://localhost:5000
- **Admin:** http://localhost:5000/admin/login

Local development uses SQLite automatically (no PostgreSQL required).

## Vercel Deployment

### Required Environment Variables

Set these in **Vercel Dashboard → Settings → Environment Variables**:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Random secret (generate: `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `DATABASE_URL` | PostgreSQL connection string (e.g. from Vercel Neon, Supabase, or Railway) |
| `ADMIN_EMAIL` | Admin login email |
| `ADMIN_PASSWORD` | Strong admin password |

### Optional Environment Variables (S3 Image Uploads)

| Variable | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret |
| `AWS_REGION` | S3 bucket region (default: `us-east-1`) |
| `AWS_S3_BUCKET` | S3 bucket name |

If S3 is not configured, image uploads will not persist across Vercel deployments.

### Deployment Steps

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables (see tables above)
4. Deploy — tables and seed data are created automatically on first request

> **Note:** If using Vercel's built-in Neon Postgres (Storage tab), it auto-injects `POSTGRES_URL`. The app accepts both `POSTGRES_URL` and `DATABASE_URL`.

## Project Structure

```
/backend
  app.py              — Flask entry point & app factory
  config.py           — Configuration from environment variables
  models.py           — SQLAlchemy models
  seed_data.py        — Starter content (only seeds empty tables)
  s3_upload.py        — S3 upload helper (production image storage)
  extensions.py       — db, login_manager instances
  /routes
    api.py            — Public JSON API
    admin.py          — Admin panel CRUD
    auth.py           — Login/logout
  /templates/admin    — Jinja2 admin templates
  /static/uploads     — Product images (local dev only)

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

/api
  index.py            — Vercel serverless entry point
```

## Design System

All styling traces back to CSS custom properties in `tokens.css`:
- **Colors:** Warm ivory background, deep forest-green primary, muted gold accents
- **Typography:** Helvetica-based system font stack
- **Spacing:** Generous whitespace, restrained and professional

## Security

- SECRET_KEY must be set via environment variable in production
- Admin passwords are hashed with bcrypt
- Secure cookies enabled automatically under HTTPS
- Security headers: X-Content-Type-Options, X-Frame-Options, Referrer-Policy
- API error responses never expose internal details
- No credentials are committed to the repository

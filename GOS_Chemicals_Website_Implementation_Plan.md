# GOS Chemicals Website — Implementation & Planning Document

This document is the complete specification for building the GOS Chemicals website. It is written so an AI coding agent (or developer) can implement the project end-to-end in an IDE without further clarification. Follow the structure, naming, and behavior exactly unless a better technical reason arises.

---

## 1. Project Summary

**Client:** GOS Chemicals — a specialty chemical manufacturer and exporter from India (Castor Oil & Derivatives, Chlorinated Paraffin Wax, Bleaching Clay, plus custom chemical manufacturing).

**Goal:** A lightweight, professional, classic, calm website with:
- A public-facing marketing site (Home, Products, Product Detail, Custom Manufacturing, Industries, FAQ, Contact)
- A custom admin panel so the client's team can add/edit/delete chemicals, industries, FAQs, and site settings without touching code
- Zero external setup — must run locally by cloning the repo and running a couple of commands. No Postgres, no Docker, no cloud DB required to run it.

**Non-goals for v1:** multi-language support, blog/news section, payment processing, user accounts for buyers. (Architecture should not block adding these later.)

---

## 2. Tech Stack (final decision)

| Layer | Choice |
|---|---|
| Frontend | Plain **HTML + CSS + JavaScript** (no framework) |
| Backend | **Python 3.10+ / Flask** |
| Database | **SQLite** via **SQLAlchemy** ORM, single file `database.db`, auto-created on first run |
| Admin panel | Server-rendered pages using **Flask + Jinja2 templates**, protected by login |
| Auth | **Flask-Login** + **bcrypt** password hashing |
| Image storage | Local `/backend/static/uploads` folder for v1 (Cloudinary can be swapped in later without changing the data model — just change how `image_url` is populated) |
| Hosting (later) | Backend: Render/Railway. Frontend can be served by the same Flask app (simplest) or split to static hosting later. |
| Env config | `.env` file (not committed) for `SECRET_KEY`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` |

**Hard constraints:**
- No hardcoded content (product names, FAQs, copy, contact info) anywhere in HTML/JS/templates. Everything renders from the database via API calls or Jinja2 context.
- The site must run with zero external services — `python app.py` after installing dependencies is the only requirement.
- `database.db` must be gitignored and auto-created + auto-seeded on first run, without ever overwriting existing data on subsequent runs.

---

## 3. Design System

### 3.1 Brand Feel
Professional, classic, calm. Industrial-B2B credibility, not flashy. No large images/animations dominating the page. Generous whitespace, restrained color, precise language already present in the source content.

### 3.2 Color Tokens
```css
:root {
  --color-bg: #FAF8F3;        /* warm off-white / ivory */
  --color-surface: #FFFFFF;
  --color-primary: #1F3A34;   /* deep forest/navy-green — trust, stability */
  --color-primary-dark: #142623;
  --color-accent: #B08D57;    /* muted gold/terracotta — used sparingly for CTAs */
  --color-text: #2B2B2B;      /* charcoal, not pure black */
  --color-text-muted: #6B6B6B;
  --color-border: #E4E0D8;
}
```

### 3.3 Typography
Helvetica-based system (no paid font license required):
```css
:root {
  --font-heading: "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-body: "Helvetica Neue", Helvetica, Arial, sans-serif;
}
```
Type scale:
- H1: 2.5rem / 700
- H2: 1.75rem / 600
- H3: 1.25rem / 600
- Body: 1rem / 400, line-height 1.6
- Small/labels: 0.875rem / 500, slight letter-spacing (used for section eyebrow labels like "FAQ", "INDUSTRIES")

### 3.4 Spacing / Layout Tokens
```css
:root {
  --spacing-section: 6rem;
  --spacing-block: 2rem;
  --radius-base: 4px;
  --max-width: 1200px;
}
```

All tokens live in one file: `/frontend/css/tokens.css`. No component should use raw hex colors or raw font names — always reference the CSS variables. This is what makes future re-theming a one-file change.

---

## 4. Repository Structure

```
/gos-chemicals
  /backend
    app.py                     # Flask app entry, creates DB + seeds data on first run
    models.py                  # SQLAlchemy models
    seed_data.py                # Starter content extracted from client's original doc
    extensions.py               # db, login_manager instances (avoid circular imports)
    config.py                   # Config class reading from .env
    /routes
      __init__.py
      api.py                    # Public JSON API blueprint
      admin.py                  # Admin panel blueprint (protected)
      auth.py                   # Login/logout routes
    /templates
      /admin
        base.html
        login.html
        dashboard.html
        chemicals_list.html
        chemical_form.html
        industries_list.html
        industry_form.html
        faqs_list.html
        faq_form.html
        settings.html
    /static
      /uploads                  # uploaded product images (gitkeep, contents gitignored)
    database.db                 # AUTO-CREATED, gitignored — not committed
    requirements.txt
    .env.example
  /frontend
    index.html                  # Home
    products.html                # Product listing
    product-detail.html          # Reads ?slug= from URL, fetches from API
    custom-manufacturing.html
    industries.html
    faq.html
    contact.html
    /css
      tokens.css                 # design tokens (colors, fonts, spacing)
      main.css                   # layout, components
    /js
      api.js                     # fetch helper functions
      nav.js                     # shared header/footer rendering (from /api/settings)
      home.js
      products.js
      product-detail.js
      faq.js
      industries.js
      contact-form.js
    /assets
      /images
  .gitignore
  README.md
```

---

## 5. Database Models (SQLAlchemy)

```python
# models.py
from extensions import db
from flask_login import UserMixin
from datetime import datetime

class Chemical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))            # "Core" or "Custom"
    summary = db.Column(db.Text)
    description = db.Column(db.Text)
    specification = db.Column(db.Text)
    applications = db.Column(db.Text)               # comma-separated values
    packaging = db.Column(db.Text)
    image_url = db.Column(db.String(300))
    cta_label = db.Column(db.String(120))
    seo_title = db.Column(db.String(200))
    seo_description = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="draft")   # draft | published
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
    key = db.Column(db.String(100), primary_key=True)   # e.g. "hero_headline"
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

class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
```

**Notes:**
- `applications` stored as comma-separated text for simplicity in v1 (avoids a join table). Frontend splits on `,` to render as tags/list. Acceptable tradeoff for a small, low-write-volume site.
- `ContactSubmission` stores every quote/enquiry request as a fallback even if email sending fails — nothing is lost.
- `status` fields (`draft`/`published`) let the admin prepare content before it goes live on the public site. Public API only returns `status="published"` records.

---

## 6. Site Settings (key-value config, editable from admin)

Seed these keys into `SiteSetting` so nothing is hardcoded in the frontend:

| Key | Example value |
|---|---|
| `site_name` | GOS Chemicals |
| `site_tagline` | Specialty Chemicals Manufactured & Exported from India |
| `hero_headline` | Specialty Chemicals Manufactured in India |
| `hero_subheadline` | Castor Oil & Derivatives \| Chlorinated Paraffin Wax \| Bleaching Clay |
| `hero_intro` | GOS Chemicals is a specialty chemical manufacturer and exporter from India... |
| `contact_email` | (client to fill) |
| `contact_phone` | (client to fill) |
| `contact_address` | (client to fill) |
| `cta_primary_label` | Request a Quote |
| `cta_secondary_label` | Explore Products |
| `seo_title_home` | Specialty Chemical Manufacturer & Exporter from India \| GOS Chemicals |
| `seo_description_home` | GOS Chemicals is a specialty chemical manufacturer and exporter from India, producing Castor Oil & Derivatives, Chlorinated Paraffin Wax and Bleaching Clay, with custom chemical manufacturing capabilities. |

Admin `/admin/settings` page: a simple form listing all keys with editable text/textarea inputs, saved on submit.

---

## 7. Seed Data (from client's original content)

`seed_data.py` should populate, only if tables are empty:

**Chemicals (Category = Core):**
1. Castor Oil & Derivatives — slug: `castor-oil-derivatives`
2. Chlorinated Paraffin Wax — slug: `chlorinated-paraffin-wax`
3. Bleaching Clay — slug: `bleaching-clay`

Use the summary/description text already present in the client's original document (see Section 12 reference content) for each.

**Industries:**
1. Paints & Coatings
2. Water Treatment
3. Mining & Mineral Processing
4. Pulp & Paper
5. Sugar Processing
6. Food, Pharmaceutical & Cosmetic Applications
7. Industrial & Specialty Chemical Applications

**FAQs:** all 8 FAQs from the original content (What products does GOS manufacture / manufacturer or trader / Castor Oil offerings / CPW / Bleaching Clay / custom chemicals / quotation info / international supply).

**Custom Manufacturing categories list** (render as a static bullet list sourced from a `SiteSetting` JSON-encoded value, or a simple dedicated table `CustomCategory` if the client is likely to edit this list — recommend a lightweight table so it's admin-editable too):
```python
class CustomCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    display_order = db.Column(db.Integer, default=0)
```
Seed with: Water-treatment chemicals, Phosphonates, Mining chemicals, Paint chemicals, Sugar-processing chemicals, Pulp & paper chemicals, Food/pharmaceutical/cosmetic ingredients, Other specialty chemical requirements.

---

## 8. Public API Endpoints

All return JSON. Only `status="published"` records are returned (except where noted).

```
GET  /api/settings                    -> { key: value, ... } for all SiteSetting rows
GET  /api/chemicals                   -> list of published chemicals, ordered by display_order
GET  /api/chemicals?category=Core     -> filter by category
GET  /api/chemicals/<slug>            -> single chemical detail (404 if not found or not published)
GET  /api/industries                  -> list of published industries, ordered
GET  /api/faqs                        -> list of published FAQs, ordered
GET  /api/custom-categories           -> list of custom manufacturing categories
POST /api/contact                     -> body: {product, specification, application, quantity,
                                          packaging, destination, name, email, message}
                                          -> saves ContactSubmission + sends email notification
                                          -> returns { success: true } or { success: false, error }
```

**CORS:** not needed if frontend is served by the same Flask app. If frontend is later split to separate static hosting, enable `flask-cors` for the frontend's domain only.

---

## 9. Admin Panel Routes

All routes below (except `/admin/login`) require `@login_required`.

```
GET/POST /admin/login
GET      /admin/logout
GET      /admin/dashboard                     -> counts: chemicals, industries, faqs, recent contact submissions

GET      /admin/chemicals                     -> table list, Edit/Delete/Add New
GET/POST /admin/chemicals/new
GET/POST /admin/chemicals/<id>/edit
POST     /admin/chemicals/<id>/delete

GET      /admin/industries
GET/POST /admin/industries/new
GET/POST /admin/industries/<id>/edit
POST     /admin/industries/<id>/delete

GET      /admin/faqs
GET/POST /admin/faqs/new
GET/POST /admin/faqs/<id>/edit
POST     /admin/faqs/<id>/delete

GET      /admin/custom-categories             -> simple list + inline add/edit/delete
GET      /admin/settings                      -> edit all SiteSetting key/values in one form
GET      /admin/contact-submissions           -> read-only list of enquiries received
```

**Chemical form fields (matches the client's real intake formula):**
Name, Slug (auto-generate from name, editable), Category (dropdown: Core/Custom), Summary (short text), Description (textarea), Specification (textarea), Applications (comma-separated input or tag input), Packaging (text), Image (file upload), CTA Label, SEO Title, SEO Description, Display Order (number), Status (dropdown: draft/published).

**Image upload handling:** save to `/backend/static/uploads/<uuid>_<filename>`, store the relative path in `image_url`. Validate file type (jpg/png/webp only) and size (< 5MB).

---

## 10. Frontend Pages & Behavior

Each public HTML page is static markup with placeholders that get filled by JS on `DOMContentLoaded`, using `api.js` helper functions.

- **`index.html`** — Hero (from `/api/settings`), 3 core chemicals (from `/api/chemicals?category=Core`), custom manufacturing teaser, industries grid (from `/api/industries`), "Why Source from Us" static section, FAQ preview (first 4 from `/api/faqs`), final CTA.
- **`products.html`** — Full list of all published chemicals (`/api/chemicals`), card grid, links to `product-detail.html?slug=...`.
- **`product-detail.html`** — Reads `slug` from query string, fetches `/api/chemicals/<slug>`, renders full detail (specification, applications, packaging, description). If not found, show a friendly "not found" state with link back to Products.
- **`custom-manufacturing.html`** — Static intro copy + dynamic list from `/api/custom-categories` + the Request/Discuss form (reuses contact form component with a "custom requirement" flag).
- **`industries.html`** — Grid from `/api/industries`.
- **`faq.html`** — Accordion from `/api/faqs`.
- **`contact.html`** — Form with fields: Product, Specification, Application, Quantity, Packaging, Destination, Name, Email, Message. POSTs to `/api/contact`. Show success/error state without page reload.

**Shared behavior (`nav.js`):** header/nav and footer content (site name, tagline, contact info in footer) rendered from `/api/settings` on every page, so a single edit in admin updates it site-wide.

**`api.js` pattern:**
```javascript
const API_BASE = '/api';

async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

async function apiPost(path, data) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}
```

Every page should handle loading and empty states gracefully (e.g., "No products available yet" rather than a blank broken layout) since content is fully dynamic.

---

## 11. Environment & First-Run Behavior

**`.env.example`:**
```
SECRET_KEY=change-this-secret-key
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=change-this-password
```

**`app.py` first-run logic:**
```python
with app.app_context():
    db.create_all()               # creates database.db + tables if not present
    seed_initial_data()           # only inserts if tables are empty — never overwrites existing data
    create_default_admin_user()   # only creates AdminUser if none exists, using .env values
```

**`.gitignore`:**
```
database.db
venv/
__pycache__/
.env
*.pyc
/backend/static/uploads/*
!/backend/static/uploads/.gitkeep
```

**Client run instructions (also goes in README.md):**
```bash
git clone <repo-url>
cd gos-chemicals/backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then edit .env with real admin email/password
python app.py
```
Site: `http://localhost:5000` — Admin: `http://localhost:5000/admin/login`

---

## 12. Reference Content (source copy to seed from)

Use the client's original document content verbatim (already supplied separately as "GOS Chemicals Home Page.docx") for:
- Hero headline/subheadline/intro text
- Each of the 3 core chemical descriptions
- The 8 custom manufacturing categories
- The 7 industries & their one-line descriptions
- The 6 "Why Source from GOS Chemicals" points (Manufacturing Capability, Product Understanding, Specification-Based Supply, Documentation, Export Coordination, Direct Communication)
- All 8 FAQs
- Footer tagline: "Specialty Chemicals Manufactured & Exported from India"

Do not paraphrase or invent new marketing claims beyond what's in the source content — the tone was deliberately kept factual/specification-based, not promotional.

---

## 13. Build Order (step-by-step for the agent)

1. Scaffold `/backend` — `app.py`, `extensions.py`, `config.py`, `models.py`, `requirements.txt`, `.env.example`
2. Implement `db.create_all()` + `seed_data.py` + default admin user creation
3. Implement auth (`/admin/login`, `/admin/logout`, `@login_required` protection)
4. Build admin CRUD for Chemicals (priority #1) — list, new, edit, delete, image upload
5. Build admin CRUD for Industries, FAQs, Custom Categories (same pattern, reuse form macros)
6. Build `/admin/settings` page (key-value editor)
7. Build `/admin/contact-submissions` read-only view
8. Build public API blueprint (`/api/...`) — all read endpoints + `/api/contact` POST
9. Build `/frontend` static pages (HTML structure + `tokens.css` + `main.css`)
10. Build `api.js` and per-page JS files to fetch and render content dynamically
11. Wire `contact.html` and custom-manufacturing form to `/api/contact`, with success/error UI
12. Seed real starter content from Section 12 reference content
13. Test full first-run flow on a clean clone (delete `database.db`, re-run, confirm auto-seed works and doesn't duplicate on second run)
14. Write final `README.md` with setup, admin usage, and deployment notes
15. (Later/optional) Deployment to Render/Railway, custom domain, swap local image storage for Cloudinary if needed

---

## 14. Acceptance Checklist

- [ ] Cloning the repo and running the 5 setup commands results in a fully working site with no manual DB setup
- [ ] No product/FAQ/industry/contact text is hardcoded anywhere in `/frontend` — everything comes from the API
- [ ] Admin can log in, add a new chemical, and see it appear on the public Products page without a code change or redeploy
- [ ] Admin can edit hero text/contact info in Settings and see it reflected in the header/footer/hero across all pages
- [ ] Contact form submissions are saved to the database even if email sending is not yet configured
- [ ] Re-running the app on an existing `database.db` never duplicates seed data or wipes admin edits
- [ ] All colors/fonts/spacing trace back to `tokens.css` variables — no raw hex/font-family values in component CSS
- [ ] Site looks and reads as professional, classic, and calm — consistent with the original document's factual, specification-based tone

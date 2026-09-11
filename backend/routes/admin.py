import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from extensions import db
from models import Chemical, Industry, FAQ, SiteSetting, CustomCategory, ContactSubmission

admin_bp = Blueprint('admin', __name__)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- Dashboard ---
@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html',
                           chemical_count=Chemical.query.count(),
                           industry_count=Industry.query.count(),
                           faq_count=FAQ.query.count(),
                           submission_count=ContactSubmission.query.count(),
                           recent_submissions=ContactSubmission.query.order_by(
                               ContactSubmission.created_at.desc()).limit(5).all())


# --- Chemicals CRUD ---
@admin_bp.route('/admin/chemicals')
@login_required
def chemicals_list():
    chemicals = Chemical.query.order_by(Chemical.display_order).all()
    return render_template('admin/chemicals_list.html', chemicals=chemicals)


@admin_bp.route('/admin/chemicals/new', methods=['GET', 'POST'])
@login_required
def chemical_new():
    if request.method == 'POST':
        chemical = Chemical()
        _populate_chemical(chemical, request)
        db.session.add(chemical)
        db.session.commit()
        flash('Chemical created.', 'success')
        return redirect(url_for('admin.chemicals_list'))
    return render_template('admin/chemical_form.html', chemical=None)


@admin_bp.route('/admin/chemicals/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def chemical_edit(id):
    chemical = Chemical.query.get_or_404(id)
    if request.method == 'POST':
        _populate_chemical(chemical, request)
        db.session.commit()
        flash('Chemical updated.', 'success')
        return redirect(url_for('admin.chemicals_list'))
    return render_template('admin/chemical_form.html', chemical=chemical)


@admin_bp.route('/admin/chemicals/<int:id>/delete', methods=['POST'])
@login_required
def chemical_delete(id):
    chemical = Chemical.query.get_or_404(id)
    db.session.delete(chemical)
    db.session.commit()
    flash('Chemical deleted.', 'success')
    return redirect(url_for('admin.chemicals_list'))


def _populate_chemical(chemical, req):
    chemical.name = req.form.get('name', '').strip()
    chemical.slug = req.form.get('slug', '').strip()
    chemical.category = req.form.get('category', 'Core')
    chemical.summary = req.form.get('summary', '')
    chemical.description = req.form.get('description', '')
    chemical.specification = req.form.get('specification', '')
    chemical.applications = req.form.get('applications', '')
    chemical.packaging = req.form.get('packaging', '')
    chemical.cta_label = req.form.get('cta_label', '')
    chemical.seo_title = req.form.get('seo_title', '')
    chemical.seo_description = req.form.get('seo_description', '')
    chemical.display_order = int(req.form.get('display_order', 0) or 0)
    chemical.status = req.form.get('status', 'draft')

    file = req.files.get('image')
    if file and file.filename and allowed_file(file.filename):
        try:
            filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            chemical.image_url = f"/static/uploads/{filename}"
        except OSError:
            from flask import flash
            flash('Image upload is not available in this environment.', 'warning')


# --- Industries CRUD ---
@admin_bp.route('/admin/industries')
@login_required
def industries_list():
    industries = Industry.query.order_by(Industry.display_order).all()
    return render_template('admin/industries_list.html', industries=industries)


@admin_bp.route('/admin/industries/new', methods=['GET', 'POST'])
@login_required
def industry_new():
    if request.method == 'POST':
        industry = Industry(
            name=request.form.get('name', '').strip(),
            description=request.form.get('description', ''),
            display_order=int(request.form.get('display_order', 0) or 0),
            status=request.form.get('status', 'published'),
        )
        db.session.add(industry)
        db.session.commit()
        flash('Industry created.', 'success')
        return redirect(url_for('admin.industries_list'))
    return render_template('admin/industry_form.html', industry=None)


@admin_bp.route('/admin/industries/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def industry_edit(id):
    industry = Industry.query.get_or_404(id)
    if request.method == 'POST':
        industry.name = request.form.get('name', '').strip()
        industry.description = request.form.get('description', '')
        industry.display_order = int(request.form.get('display_order', 0) or 0)
        industry.status = request.form.get('status', 'published')
        db.session.commit()
        flash('Industry updated.', 'success')
        return redirect(url_for('admin.industries_list'))
    return render_template('admin/industry_form.html', industry=industry)


@admin_bp.route('/admin/industries/<int:id>/delete', methods=['POST'])
@login_required
def industry_delete(id):
    industry = Industry.query.get_or_404(id)
    db.session.delete(industry)
    db.session.commit()
    flash('Industry deleted.', 'success')
    return redirect(url_for('admin.industries_list'))


# --- FAQs CRUD ---
@admin_bp.route('/admin/faqs')
@login_required
def faqs_list():
    faqs = FAQ.query.order_by(FAQ.display_order).all()
    return render_template('admin/faqs_list.html', faqs=faqs)


@admin_bp.route('/admin/faqs/new', methods=['GET', 'POST'])
@login_required
def faq_new():
    if request.method == 'POST':
        faq = FAQ(
            question=request.form.get('question', '').strip(),
            answer=request.form.get('answer', '').strip(),
            display_order=int(request.form.get('display_order', 0) or 0),
            status=request.form.get('status', 'published'),
        )
        db.session.add(faq)
        db.session.commit()
        flash('FAQ created.', 'success')
        return redirect(url_for('admin.faqs_list'))
    return render_template('admin/faq_form.html', faq=None)


@admin_bp.route('/admin/faqs/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def faq_edit(id):
    faq = FAQ.query.get_or_404(id)
    if request.method == 'POST':
        faq.question = request.form.get('question', '').strip()
        faq.answer = request.form.get('answer', '').strip()
        faq.display_order = int(request.form.get('display_order', 0) or 0)
        faq.status = request.form.get('status', 'published')
        db.session.commit()
        flash('FAQ updated.', 'success')
        return redirect(url_for('admin.faqs_list'))
    return render_template('admin/faq_form.html', faq=faq)


@admin_bp.route('/admin/faqs/<int:id>/delete', methods=['POST'])
@login_required
def faq_delete(id):
    faq = FAQ.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    flash('FAQ deleted.', 'success')
    return redirect(url_for('admin.faqs_list'))


# --- Custom Categories ---
@admin_bp.route('/admin/custom-categories', methods=['GET', 'POST'])
@login_required
def custom_categories():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            cat = CustomCategory(
                name=request.form.get('name', '').strip(),
                display_order=int(request.form.get('display_order', 0) or 0),
            )
            db.session.add(cat)
            db.session.commit()
            flash('Category added.', 'success')
        elif action == 'delete':
            cat_id = request.form.get('id')
            cat = CustomCategory.query.get(cat_id)
            if cat:
                db.session.delete(cat)
                db.session.commit()
                flash('Category deleted.', 'success')
        return redirect(url_for('admin.custom_categories'))
    cats = CustomCategory.query.order_by(CustomCategory.display_order).all()
    return render_template('admin/custom_categories.html', categories=cats)


# --- Settings ---
@admin_bp.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        all_settings = SiteSetting.query.all()
        for s in all_settings:
            new_val = request.form.get(s.key, '')
            s.value = new_val
        db.session.commit()
        flash('Settings saved.', 'success')
        return redirect(url_for('admin.settings'))
    all_settings = SiteSetting.query.order_by(SiteSetting.key).all()
    return render_template('admin/settings.html', settings=all_settings)


# --- Contact Submissions ---
@admin_bp.route('/admin/contact-submissions')
@login_required
def contact_submissions():
    submissions = ContactSubmission.query.order_by(ContactSubmission.created_at.desc()).all()
    return render_template('admin/contact_submissions.html', submissions=submissions)

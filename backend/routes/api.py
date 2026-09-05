from flask import Blueprint, request, jsonify
from models import Chemical, Industry, FAQ, SiteSetting, CustomCategory, ContactSubmission
from extensions import db

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/settings')
def get_settings():
    settings = SiteSetting.query.all()
    return jsonify({s.key: s.value for s in settings})


@api_bp.route('/chemicals')
def get_chemicals():
    query = Chemical.query.filter_by(status='published').order_by(Chemical.display_order)
    category = request.args.get('category')
    if category:
        query = query.filter_by(category=category)
    chemicals = query.all()
    return jsonify([_chemical_to_dict(c) for c in chemicals])


@api_bp.route('/chemicals/<slug>')
def get_chemical(slug):
    chemical = Chemical.query.filter_by(slug=slug, status='published').first()
    if not chemical:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(_chemical_to_dict(chemical))


@api_bp.route('/industries')
def get_industries():
    industries = Industry.query.filter_by(status='published').order_by(Industry.display_order).all()
    return jsonify([{'id': i.id, 'name': i.name, 'description': i.description} for i in industries])


@api_bp.route('/faqs')
def get_faqs():
    faqs = FAQ.query.filter_by(status='published').order_by(FAQ.display_order).all()
    return jsonify([{'id': f.id, 'question': f.question, 'answer': f.answer} for f in faqs])


@api_bp.route('/custom-categories')
def get_custom_categories():
    cats = CustomCategory.query.order_by(CustomCategory.display_order).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in cats])


@api_bp.route('/contact', methods=['POST'])
def submit_contact():
    data = request.get_json(silent=True) or {}
    required = ['name', 'email']
    for field in required:
        if not data.get(field, '').strip():
            return jsonify({'success': False, 'error': f'{field} is required'}), 400

    submission = ContactSubmission(
        product=data.get('product', ''),
        specification=data.get('specification', ''),
        application=data.get('application', ''),
        quantity=data.get('quantity', ''),
        packaging=data.get('packaging', ''),
        destination=data.get('destination', ''),
        name=data.get('name', ''),
        email=data.get('email', ''),
        message=data.get('message', ''),
    )
    db.session.add(submission)
    db.session.commit()
    return jsonify({'success': True})


def _chemical_to_dict(c):
    return {
        'id': c.id,
        'slug': c.slug,
        'name': c.name,
        'category': c.category,
        'summary': c.summary,
        'description': c.description,
        'specification': c.specification,
        'applications': c.applications,
        'packaging': c.packaging,
        'image_url': c.image_url,
        'cta_label': c.cta_label,
        'seo_title': c.seo_title,
        'seo_description': c.seo_description,
    }

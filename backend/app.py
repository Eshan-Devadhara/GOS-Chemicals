import os
import sys
import traceback
from flask import Flask, send_from_directory, jsonify
import bcrypt
from config import Config
from extensions import db, login_manager
from models import AdminUser


def create_app():
    instance_path = os.path.abspath('/tmp/gos_chemicals_instance') if os.getenv('VERCEL') else None

    if instance_path:
        try:
            os.makedirs(instance_path, exist_ok=True)
        except OSError:
            pass
        app = Flask(
            __name__,
            static_folder='static',
            template_folder='templates',
            instance_path=instance_path
        )
    else:
        app = Flask(
            __name__,
            static_folder='static',
            template_folder='templates'
        )

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(AdminUser, int(user_id))

    # Register blueprints
    from routes.api import api_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Serve frontend static files
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')
    frontend_dir = os.path.normpath(frontend_dir)

    @app.route('/')
    def serve_index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/<path:filename>')
    def serve_frontend(filename):
        try:
            return send_from_directory(frontend_dir, filename)
        except Exception:
            return send_from_directory(frontend_dir, 'index.html')

    # --- Security Headers ---
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    # --- Error Handlers (production-safe) ---
    @app.errorhandler(404)
    def not_found(e):
        if _is_api_request():
            return jsonify({'error': 'Not found'}), 404
        try:
            return send_from_directory(frontend_dir, 'index.html'), 404
        except Exception:
            return '<h1>404 — Page Not Found</h1>', 404

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f'Internal server error: {e}', exc_info=True)
        if _is_api_request():
            return jsonify({'error': 'Internal server error'}), 500
        return '<h1>500 — Internal Server Error</h1>', 500

    return app


def _is_api_request():
    """Check if the current request is for an API endpoint."""
    from flask import request
    return request.path.startswith('/api/')


def initialize_database(app):
    with app.app_context():
        try:
            db.create_all()

            # Idempotent schema migration for cloudinary_public_id
            try:
                from sqlalchemy import inspect, text
                inspector = inspect(db.engine)
                columns = [col['name'] for col in inspector.get_columns('chemical')]
                if 'cloudinary_public_id' not in columns:
                    db.session.execute(text('ALTER TABLE chemical ADD COLUMN cloudinary_public_id VARCHAR(300)'))
                    db.session.commit()
                    app.logger.info("Migrated schema: added cloudinary_public_id to chemical table")
                
                # Idempotent schema migration for deleted_at on contact_submission
                cs_columns = [col['name'] for col in inspector.get_columns('contact_submission')]
                if 'deleted_at' not in cs_columns:
                    db.session.execute(text('ALTER TABLE contact_submission ADD COLUMN deleted_at TIMESTAMP'))
                    db.session.commit()
                    app.logger.info("Migrated schema: added deleted_at to contact_submission table")
            except Exception as e:
                app.logger.error(f"Schema migration error: {e}", exc_info=True)

            # Seed data only if tables are empty
            from seed_data import seed_initial_data
            seed_initial_data()

            # Create default admin user if none exists
            if AdminUser.query.count() == 0:
                admin_password = app.config['ADMIN_PASSWORD']
                if admin_password in ('change-this-password', 'admin123', 'password', ''):
                    app.logger.warning(
                        'ADMIN_PASSWORD is not set or uses a default value. '
                        'Set a strong password via the ADMIN_PASSWORD environment variable.'
                    )
                hashed = bcrypt.hashpw(
                    admin_password.encode('utf-8'),
                    bcrypt.gensalt()
                ).decode('utf-8')
                admin = AdminUser()
                admin.email = app.config['ADMIN_EMAIL']
                admin.password_hash = hashed
                db.session.add(admin)
                db.session.commit()
                app.logger.info(f"Default admin user created: {app.config['ADMIN_EMAIL']}")
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            app.logger.error(f"Database initialization failed: {e}", exc_info=True)
            raise

    # Ensure uploads directory exists (skip on read-only filesystems like Vercel)
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError:
        pass


if __name__ == '__main__':
    app = create_app()
    initialize_database(app)
    print("Server running at http://localhost:5000")
    print("Admin panel at http://localhost:5000/admin/login")
    app.run(debug=True, port=5000)

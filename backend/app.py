import os
from flask import Flask, send_from_directory
import bcrypt
from config import Config
from extensions import db, login_manager
from models import AdminUser


def create_app():
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(int(user_id))

    # Register blueprints
    from routes.api import api_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Serve frontend static files
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

    @app.route('/')
    def serve_index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/<path:filename>')
    def serve_frontend(filename):
        try:
            return send_from_directory(frontend_dir, filename)
        except Exception:
            return send_from_directory(frontend_dir, 'index.html')

    return app


def initialize_database(app):
    with app.app_context():
        db.create_all()

        # Seed data only if tables are empty
        from seed_data import seed_initial_data
        seed_initial_data()

        # Create default admin user if none exists
        if AdminUser.query.count() == 0:
            hashed = bcrypt.hashpw(
                app.config['ADMIN_PASSWORD'].encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
            admin = AdminUser(email=app.config['ADMIN_EMAIL'], password_hash=hashed)
            db.session.add(admin)
            db.session.commit()
            print(f"Default admin user created: {app.config['ADMIN_EMAIL']}")

    # Ensure uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


if __name__ == '__main__':
    app = create_app()
    initialize_database(app)
    print("Server running at http://localhost:5000")
    print("Admin panel at http://localhost:5000/admin/login")
    app.run(debug=True, port=5000)

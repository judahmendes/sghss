import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.models import db
from src.routes.auth import auth_bp
from src.routes.patient import patient_bp
from src.config import config
from src.utils import setup_logging, SGHSSBaseException
import logging

# Setup logging
logger = setup_logging()

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, origins="*")  # Allow all origins for development - change in production
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patient_bp, url_prefix='/api')
    
    # Register error handlers
    @app.errorhandler(SGHSSBaseException)
    def handle_custom_exception(error):
        """Handle custom SGHSS exceptions"""
        logger.error(f"Custom exception: {error.message}")
        return jsonify({'error': error.message}), error.status_code
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle bad request errors"""
        logger.warning(f"Bad request: {error}")
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(401)
    def handle_unauthorized(error):
        """Handle unauthorized errors"""
        logger.warning(f"Unauthorized access: {error}")
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(403)
    def handle_forbidden(error):
        """Handle forbidden errors"""
        logger.warning(f"Forbidden access: {error}")
        return jsonify({'error': 'Forbidden'}), 403
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle not found errors"""
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(422)
    def handle_unprocessable_entity(error):
        """Handle validation errors"""
        logger.warning(f"Validation error: {error}")
        return jsonify({'error': 'Validation failed'}), 422
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle internal server errors"""
        logger.error(f"Internal server error: {error}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is required'}), 401
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return {'status': 'healthy', 'message': 'SGHSS API is running'}, 200
    
    # Create database tables
    with app.app_context():
        # Ensure database directory exists
        db_dir = os.path.join(os.path.dirname(__file__), 'database')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

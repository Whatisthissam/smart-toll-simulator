import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    # Keep it simple, initializing Flask app
    app = Flask(__name__, static_folder='../frontend', static_url_path='/')
    CORS(app) # Enable CORS for all routes

    # Register blueprints (routes)
    from routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Serve Frontend Files
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('../frontend', path)

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    # Run the application
    app.run(debug=True, port=port)

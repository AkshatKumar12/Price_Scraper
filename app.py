from flask import Flask
from config import Config
from database import engine, Base
from routes.search import search_bp
from routes.compare import compare_bp
from routes.products import product_bp
from routes.health import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Base.metadata.create_all(bind=engine)

    app.register_blueprint(search_bp)
    app.register_blueprint(compare_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(health_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

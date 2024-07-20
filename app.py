import os
import logging
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from blocklist import BLOCKLIST
import models
from db import db
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBluePrint

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1.2"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    logging.basicConfig(level=logging.DEBUG)
    CORS(app)
    try:
        db.init_app(app)
        api = Api(app)

        app.config["JWT_SECRET_KEY"] = "211417960297026057261900564916763605453"
        jwt = JWTManager(app)

        @jwt.token_in_blocklist_loader
        def check_if_token_in_blocklist(jwt_header, jwt_payload):
            return jwt_payload["jti"] in BLOCKLIST

        @jwt.revoked_token_loader
        def revoked_token_callback(jwt_header, jwt_payload):
            return (
                jsonify(
                    {"description": "The token has been revoked.", "error": "token_revoked"}
                ),
                401,
            )

        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            return (
                jsonify({"message": "The token has expired.", "error": "token_expired"}),
                401,
            )

        @jwt.invalid_token_loader
        def invalid_token_callback(error):
            return (
                jsonify({"message": "Signature verification failed.", "error": "invalid_token"}),
                401,
            )

        @jwt.unauthorized_loader
        def missing_token_callback(error):
            return (
                jsonify({"description": "Request does not contain an access token.",
                         "error": "authorization_required"}),
                401,
            )

        with app.app_context():
            logging.debug("Creating all database tables.")
            db.create_all()

        logging.debug("Registering blueprints.")
        api.register_blueprint(ItemBlueprint)
        api.register_blueprint(StoreBlueprint)
        api.register_blueprint(TagBlueprint)
        api.register_blueprint(UserBluePrint)

        @app.errorhandler(500)
        def internal_error(error):
            return {"error": str(error)}, 500

        @app.errorhandler(404)
        def not_found_error(error):
            return {"error": "Not Found"}, 404

    except Exception as e:
        logging.error(f"An error occurred while creating the app: {e}")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

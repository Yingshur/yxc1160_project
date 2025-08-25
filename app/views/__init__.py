from .emperor import emperor_bp
from .war import war_bp
from .admin import admin_bp
from .chatbot import chatbot_bp
from .version_control import version_control_bp
from .home import home_bp
from .login_logout import login_logout_bp
from .image import image_bp
from .architecture import architecture_bp
from .literature import literature_bp
from .artifact import artifact_bp

from flask import Blueprint
def blueprint_registration(app):
    app.register_blueprint(emperor_bp)
    app.register_blueprint(war_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(version_control_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(login_logout_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(architecture_bp)
    app.register_blueprint(literature_bp)
    app.register_blueprint(artifact_bp)



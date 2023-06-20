from flask import Flask
from config import DevelopmentConfig
from database import db
from controllers.user_controller import bp_user
from controllers.work_category_controller import bp_category
from controllers.work_data_controller import bp_work_data
from controllers.team_controller import bp_team
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

app.register_blueprint(bp_user)
app.register_blueprint(bp_category)
app.register_blueprint(bp_work_data)
app.register_blueprint(bp_team)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

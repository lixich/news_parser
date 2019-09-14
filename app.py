import scheduler
from flask import Flask
from flask_cors import CORS
from handlers import register_blueprints

scheduler.init()
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, supports_credentials=True)
register_blueprints(app)

if __name__ == "__main__":
    app.run()

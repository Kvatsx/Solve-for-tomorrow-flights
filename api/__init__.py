from flask import Flask

from api.routes.routes import mod
from api.database import mongo

app = Flask(__name__)
config_object = 'api.settings'
app.config.from_object(config_object)

mongo.init_app(app)

app.register_blueprint(routes.routes.mod, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from web.baas import baas
from web.configs import configs

if __name__ == '__main__':
    app = Flask(__name__, static_folder='web/static', static_url_path='/static')
    app.register_blueprint(baas)
    app.register_blueprint(configs)
    app.run(debug=False, port=1117)

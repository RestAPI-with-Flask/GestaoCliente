from flask import Flask
from controller.api import api
from controller.web import web


app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta'
app.json.sort_keys = False


# Adicionando Routers
app.register_blueprint(api)
app.register_blueprint(web)


@app.route('/hello')
def hello():
    return {
        'message': 'Hello World'
    }


if __name__ == '__main__':
    app.run(debug=True)

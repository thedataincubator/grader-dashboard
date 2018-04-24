from flask import Flask, request, render_template, request

def create_app(db_uri, brand):

    app = Flask(__name__)

    def render_with_brand(route, **kwargs):
        return render_template(route, brand=brand, **kwargs)

    @app.route('/')
    def index():
        return render_with_brand('index.html')


    return app
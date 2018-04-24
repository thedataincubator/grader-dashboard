from flask import Flask, request, render_template, request
from .models import db
from .gradeservice import GradeService

def create_app(db_uri, brand):

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)

    gs = GradeService(db)

    def render_with_brand(route, **kwargs):
        return render_template(route, brand=brand, **kwargs)

    @app.route('/')
    def index():
        subs = gs.overview()
        return render_with_brand('index.html', subs=subs)

    @app.route('/student/<student>')
    def student_overview(student):
        info = gs.student_overview(student)
        return render_with_brand('student_overview', info=info)

    return app
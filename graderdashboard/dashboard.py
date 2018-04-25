from collections import defaultdict
from itertools import chain
from datetime import datetime
from flask import Flask, request, render_template, request
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.layouts import column
from .models import db
from .gradeservice import GradeService

def _flatten(x):
    return tuple(chain.from_iterable(x))

PROJECTS = {
    'dw':['summary_statistics', 'most_common_item', 'items_by_region', 'script_anomalies', 'script_growth', 'rare_scripts'],
    'in':['problem1', 'problem2'],
    'ip':['mersenne_numbers', 'lucas_lehmer', 'mersenne_primes', 'is_prime_fast', 'erastosthenes'],
    'pw':['summary_statistics', 'most_common_item', 'items_by_region'],
    'vc':['point_repr', 'add_subtract', 'multiplication', 'distance', 'k_means'],
    'ml':['billing_model', 'balanced_billing_model', 'demo_model', 'ensemble_model'] 
}

def create_app(db_uri, brand):

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)

    gs = GradeService(db)

    def render_with_brand(route, **kwargs):
        return render_template(route, brand=brand, **kwargs)

    def _plot_subs(overview):
        days = list(overview.keys())
        subs = [overview[i] for i in days]

        p1 = figure(x_axis_type='datetime', plot_height=250,
                    title='Submissions per Day')
        plot_days = [datetime.strptime(i, "%Y-%m-%d") for i in days]
        p1.line(plot_days, subs)
        p1.circle(plot_days, subs)
        return p1

    @app.route('/')
    def index():
        overview = gs.day_overview()
        script, div = components(_plot_subs(overview))
        return render_with_brand('index.html', 
                                 div=div,
                                 script=script)

    @app.route('/students')
    def students():
        subs = gs.overview()
        return render_with_brand('students.html', subs=subs)

    @app.route('/questions')
    def questions():
        eles = gs.question_overview()
        return render_with_brand('questions.html', eles=eles)

    @app.route('/question/<question>')
    def questeion_overview(question):
        # TODO page for each project
        overview = gs.question_info(question)
        per_student = gs.project_per_student(question)
        total_submissions = sum(overview.values())
        p = _plot_subs(overview)
        script, div = components(p)
        return render_with_brand('question_overview.html',
                                 info=per_student,
                                 question=question,
                                 script=script,
                                 div=div)

    @app.route('/student/<student>')
    def student_overview(student):
        per_project = gs.student_per_project(student)
        overview = gs.student_overview(student)
        total_submissions = sum(overview.values())
        p1 = _plot_subs(overview)

        projects = defaultdict(dict)
        for i in per_project:
            project = i['problem'].split('__')[0]
            projects[project][i['problem']] = i['score']

        p_names = sorted(PROJECTS.keys())
        x = _flatten([[(k, str(i)) for i, j in enumerate(PROJECTS[k])] for k in p_names])
        scores = _flatten([[projects[k].get("{}__{}".format(k, j), 0) for j in PROJECTS[k]] for k in p_names])
        source = ColumnDataSource(data=dict(x=x, 
                                            scores=scores))
        p = figure(x_range=FactorRange(*x), plot_height=150)
        p.vbar(x='x', top='scores', source=source, width=0.9)
        
        script, div = components(column(p1, p))
        return render_with_brand('student_overview.html', 
                                 info=per_project, 
                                 script=script, 
                                 div=div,
                                 name=student,
                                 total=total_submissions)

    return app
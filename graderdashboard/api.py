from collections import defaultdict
from flask import request, jsonify
from flask_security import login_required

def add_v1_api_endpoints(app, gs):

    def route(path, **kwargs):
        return app.route('/api/v1' + path, **kwargs)

    @route('/students')
    @login_required
    def api_v1_students():
        return jsonify(gs.overview())

    @route('/questions')
    @login_required
    def api_v1_questions():
        return jsonify(gs.question_overview())

    @route('/question/<question>')
    @login_required
    def api_v1_questeion_overview(question):
        # TODO page for each project
        overview = gs.question_info(question)
        per_student = gs.project_per_student(question)
        total_submissions = sum(overview.values())
        return jsonify(dict(
            overview=overview,
            per_student=per_student,
            total_submissions=total_submissions
        ))

    @route('/student/<student>')
    @login_required
    def api_v1_student_overview(student):
        per_project = gs.student_per_project(student)
        overview = gs.student_overview(student)
        total_submissions = sum(overview.values())

        projects = defaultdict(dict)
        for i in per_project:
            project = i['problem'].split('__')[0]
            projects[project][i['problem']] = i['score']

        return jsonify(dict(
            overview=overview,
            total_submissions=total_submissions,
            projects=projects
        ))
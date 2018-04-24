from .models import Grade

class GradeService():

    def __init__(self, db):
        self.db = db
        self._s = self.db.session

    def overview(self):
        submissions =  self._s.query(Grade.name, 
                             self.db.func.count(Grade.submission_time)) \
                             .group_by(Grade.name) \
                             .order_by(self.db.desc(self.db.func.count(Grade.submission_time))) \
                             .all()

        return [{'name': i[0], 'subs': i[1]} for i in submissions]

    def student_per_project(self):
        pass

    def project_overview(self):
        pass

    def student_overview(self, student):
        s = self._s.query(Grade.question, self.db.func.max(Grade.score)) \
                          .filter(Grade.name == student) \
                         .group_by(Grade.question).all()
        return [{'problem': i[0], 'score': i[1]} for i in s]



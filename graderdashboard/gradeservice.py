from collections import defaultdict
from .models import Grade

class GradeService():

    def __init__(self, db):
        self.db = db
        self._s = self.db.session

    def _count_days(self, s, index=1):
        d = defaultdict(int)
        for i in s:
            day = i[index].strftime("%Y-%m-%d")
            d[day] += 1
        return d

    def day_overview(self):
        s = self._s.query(Grade.question, Grade.submission_time)
        return self._count_days(s)

    def overview(self):
        submissions =  self._s.query(Grade.name, 
                             self.db.func.count(Grade.submission_time)) \
                             .group_by(Grade.name) \
                             .order_by(self.db.desc(self.db.func.count(Grade.submission_time))) \
                             .all()

        return [{'name': i[0], 'subs': i[1]} for i in submissions]

    def student_overview(self, student):
        s = self._s.query(Grade.question, Grade.submission_time) \
                          .filter(Grade.name == student)
        return self._count_days(s)

    def student_per_project(self, student):
        s = self._s.query(Grade.question, 
                          self.db.func.max(Grade.score), 
                          self.db.func.count(Grade.submission_time)) \
                          .filter(Grade.name == student) \
                          .group_by(Grade.question).all()
        
        return [{'problem': i[0], 'score': i[1], 'count' :i[2]} for i in s]

    def question_overview(self):
        s = self._s.query(Grade.question,
                          self.db.func.avg(Grade.score),
                          self.db.func.count(Grade.submission_time)) \
                          .group_by(Grade.question).all()

        return [{'problem': i[0], 'mean': i[1], 'count': i[2]} for i in s]

    def question_info(self, question):
        s = self._s.query(Grade.score, Grade.submission_time) \
                    .filter(Grade.question == question)
        return self._count_days(s)

    def project_per_student(self, question):
        s = self._s.query(Grade.name,
                          self.db.func.max(Grade.score),
                          self.db.func.count(Grade.submission_time)) \
                          .filter(Grade.question == question) \
                          .group_by(Grade.name)
        return [{'name': i[0], 'score': i[1], 'count': i[2]} for i in s]

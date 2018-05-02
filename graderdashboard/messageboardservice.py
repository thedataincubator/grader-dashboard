from .models import Post

class MessageBoardService(object):
    def __init__(self, db):
        self.db = db
        self._s = self.db.session

    def recent_post_count(self):
        return self._s.query(self.db.func.count(Post.post_id)) \
                      .group_by(self.db.func.strftime('%W', Post.post_time)) \
                      .order_by(self.db.func.strftime('%W', Post.post_time).desc()) \
                      .first()[0]

    def recent_thread_count(self):
        return self._s.query(self.db.func.count(self.db.distinct(Post.parent))) \
                      .group_by(self.db.func.strftime('%W', Post.post_time)) \
                      .order_by(self.db.func.strftime('%W', Post.post_time).desc()) \
                      .first()[0]

    def recent_poster_count(self):
        return self._s.query(self.db.func.count(self.db.distinct(Post.user_name))) \
                      .group_by(self.db.func.strftime('%W', Post.post_time)) \
                      .order_by(self.db.func.strftime('%W', Post.post_time).desc()) \
                      .first()[0]

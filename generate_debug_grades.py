from graderdashboard.dashboard import PROJECTS
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
import random
NAMES = ['sally', 'ben', 'sara', 'bob', 'schoolbus', 'apple', 'pear',
         'carol', 'silly_guy', 'humpty_dumpty', 'sammy']

def generate_fake_names():
    return ["{}@gmail.com".format(i) for i in NAMES]

def generate_grades(people):
    now = datetime.now()
    grades = []
    for k, v in PROJECTS.items():
        for project in v:
            for person in people:
                for n in range(random.randint(0, 45)):

                    grades.append({'name':person,
                                   'question':"{}__{}".format(k, project),
                                   'score': random.random(),
                                   'submission_time': now + timedelta((random.random() - .5)*10)})
    return grades

def generate_threads(n_threads):
    create_time = [datetime.now() - timedelta(days=random.randint(0, 30))
                   for _ in range(n_threads)]

    return list(enumerate(create_time))

def generate_posts(n_posts, threads, people):
    posts = []
    for i in range(n_posts):
        if i < len(threads):
            parent, post_time = threads[i]
        else:
            parent, thread_time = random.choice(threads)
            post_time = thread_time + timedelta(days=random.randint(0, 30))
        posts.append({'post_id': i,
                      'parent': parent,
                      'post_time': post_time,
                      'user_name': random.choice(people)})

    return posts

def main():
    people = generate_fake_names()
    grades = generate_grades(people)
    grades_df = pd.DataFrame(grades).sort_values(by='submission_time')
    threads = generate_threads(20)
    posts = generate_posts(100, threads, people)
    posts_df = pd.DataFrame(posts).sort_values(by='post_time')
    connection = sqlite3.connect("grades.db")
    grades_df.to_sql('grades', connection)
    posts_df.to_sql('posts', connection)


if __name__ == '__main__':
    main()

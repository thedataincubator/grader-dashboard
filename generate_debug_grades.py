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





def main():
    people = generate_fake_names()
    grades = generate_grades(people)
    df = pd.DataFrame(grades).sort_values(by='submission_time')
    connection = sqlite3.connect("grades.db")
    df.to_sql('grades', connection)
    


if __name__ == '__main__':
    main()
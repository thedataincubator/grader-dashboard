import pandas as pd
import sqlite3

def main():
    posts_df = pd.read_csv('~/Downloads/posts.csv')
    connection = sqlite3.connect("grades.db")
    posts_df.to_sql('posts', connection)


if __name__ == '__main__':
    main()

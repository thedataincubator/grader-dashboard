import os
from graderdashboard import create_app

DB_URI = os.environ.get('DB_URI', None)
BRAND = os.environ.get('BRAND', 'WQU')

app = create_app(DB_URI, BRAND)

if __name__ == '__main__':
    app.run(port=5000)
import os
from graderdashboard import create_app

DB_URI = os.environ.get('DB_URI', None)
BRAND = os.environ.get('BRAND', 'TEST')
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')

app = create_app(DB_URI, BRAND, SECRET_KEY)

if __name__ == '__main__':
    app.run(port=5000)
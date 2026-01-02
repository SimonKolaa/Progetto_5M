# run.py
# UGUALE a quello del prof
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
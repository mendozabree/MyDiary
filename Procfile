web: gunicorn --workers=1 run:app heroku ps:scale web=1
release: python api/v1/database.py db upgrade
# Deployment Notes

## GitHub
Repository:
https://github.com/mdpos95-tech/volunteerhub_MOD5

## Render
Web Service:


## Database
Provider: Render PostgreSQL
Region: Frankfurt

## Render Commands
Build Command:
bash build.sh

Start Command:
gunicorn volunteerhub.wsgi:application

## Environment Variables Used:
-SECRET_KEY
-DEBUG
-DATABASE_URL
-BREVO_API_KEY

## Testing
python manage.py check
python manage.py test accounts

12 automated tests passing.
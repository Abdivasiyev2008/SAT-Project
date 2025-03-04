# Python 3.12.6 image bazasida Django uchun
FROM python:3.12.6-slim

# Ishchi katalogni belgilash
WORKDIR /app

# Python paketlarni o'rnatish
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Django loyihasini konteynerga nusxalash
COPY . .

# Static fayllarni to'plash
RUN python manage.py collectstatic --noinput

# Django ilovasini ishga tushirish
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV DJANGO_SETTINGS_MODULE=demo_minio.settings
EXPOSE 8000
CMD ["bash","-lc","python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

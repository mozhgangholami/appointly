FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY media_seed /code/media_seed
COPY entrypoint.sh /code/entrypoint.sh

RUN sed -i 's/\r$//' /code/entrypoint.sh && chmod +x /code/entrypoint.sh

ENTRYPOINT ["/code/entrypoint.sh"]

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
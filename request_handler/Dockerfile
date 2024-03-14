FROM python:3.10.13

ENV PYTHONUNBUFFERED=1

WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .

CMD ["flask", "--app", "main.py", "run", "--host", "0.0.0.0"]
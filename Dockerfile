FROM python:3.9
WORKDIR /app

COPY requirements.txt requirements.txt
COPY app.py app.py
COPY mostrans_data.xlsx mostrans_data.xlsx

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask

RUN touch /app/app.log
RUN ls -la /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run"]

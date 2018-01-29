FROM python:2-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_DEBUG 1
ENV FLASK_APP src/hello.py
CMD [ "flask", "run", "--host=0.0.0.0" ]
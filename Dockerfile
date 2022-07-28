FROM python:3.10
LABEL maintainer="Stephen Humer"

COPY ./techtrends /app
WORKDIR /app
RUN pip install -r requirements.txt && python init_db.py

EXPOSE 3111

CMD [ "python", "app.py" ]
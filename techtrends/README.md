# TechTreds Web Application

This is a Flask application that lists the latest articles within the cloud-native ecosystem.

## Run as Python application

To run this application there are 3 steps required:

1. Initialize the database by using the `python init_db.py` command. This will create or overwrite the `database.db` file that is used by the web application.
2. Install application requirements by using the `pip install -r requirements.txt` command. This will install Flask, among other dependencies.
3. Run the TechTrends application by using the `python app.py` command. The application is running on port `3111` and you can access it by querying the `http://127.0.0.1:3111/` endpoint.

## Run as Docker container

1. Create a docker image by using the `docker build -t techtrends:techtrends .` command.
2. Run the docker image from step 1 as a docker container using the `docker run -d -p 7111:3111 --name techtrends techtrends:techtrends` command. You can access it by quering the `http://127.0.0.1:7111/ endpoint. 
